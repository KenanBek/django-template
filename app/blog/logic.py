import urllib2
import urlparse

from bs4 import BeautifulSoup

from django.db.models import Q
from django.shortcuts import get_object_or_404

from core import abstracts
from . import models


class BlogLogic(abstracts.LogicAbstract):
    def __init__(self, request):
        super(BlogLogic, self).__init__(request)

    def page(self, page_slug):
        return get_object_or_404(models.Page, slug=page_slug, status=models.ITEM_STATUS_PUBLISHED)

    def pages(self, page_number=None):
        return models.Page.objects.filter(status=models.ITEM_STATUS_PUBLISHED).all()

    def post(self, post_id, post_slug):
        return get_object_or_404(models.Post, pk=post_id, slug=post_slug, status=models.ITEM_STATUS_PUBLISHED)

    def posts(self, page_number=None):
        return models.Post.objects.filter(status=models.ITEM_STATUS_PUBLISHED).order_by('-modified_at').all()

    def search(self, term):
        pages = models.Page.objects.filter(Q(title__contains=term) | Q(content__contains=term))
        posts = models.Post.objects.filter((Q(title__contains=term)
                                            | Q(short_content__contains=term)
                                            | Q(full_content__contains=term))
                                           & Q(status=models.ITEM_STATUS_PUBLISHED))
        return {
            "pages": pages,
            "posts": posts
        }

    def new_subscription(self, name, email):
        subscriber = models.Subscriber()
        subscriber.name = name
        subscriber.email = email
        subscriber.save()


''' The Open Graph Protocol '''


class WebPage(object):
    def __init__(self, success=None, content=None, status=None, message=None):
        self.success = success
        self.status = status
        self.message = message
        self.content = content


class WebInspector(object):
    def __init__(self, success=None, web_link=None, message=None):
        self.success = success
        self.web_link = web_link
        self.message = message


class Helper(object):
    @staticmethod
    def encode_string(s):
        if isinstance(s, str):
            return unicode(s, 'utf-8')
        elif isinstance(s, unicode):
            return s.encode('utf-8')
        else:
            raise Exception(u"Incorrect input parameter for string encoder")

    @staticmethod
    def get_page_by_url(url):
        try:
            encoded_url = Helper.encode_string(url)
            request = urllib2.Request(url=encoded_url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64)"})
            page_stream = urllib2.urlopen(request, timeout=5)
            if page_stream.url != encoded_url:
                message = u"redirect to {}".format(page_stream.url)
                return WebPage(success=False, message=message)
            else:
                content = page_stream.read()
                encoded_content = Helper.encode_string(content)
                return WebPage(success=True, status=page_stream.code, content=encoded_content)
        except urllib2.HTTPError as e:
            return WebPage(success=False, status=e.code, message=e.msg)
        except Exception as e:
            return WebPage(success=False, message=repr(e))

    @staticmethod
    def clean_array(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    @staticmethod
    def fix_url(parent_url, url):
        url = url.lower()
        source_url = parent_url.lower()
        parsed_uri = urlparse.urlparse(source_url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        result = urlparse.urljoin(domain, url)
        return result


class OpenGraphLogic(object):
    url = None

    def __init__(self, url):
        self.url = url

    def _get_web_link(self):
        web_link = models.WebLink()
        web_link.url = self.url
        web_links = models.WebLink.objects.filter(url=self.url).order_by('-version').all()
        if web_links.count():
            self.version = web_links[0].version + 1
        else:
            self.version = 1
        web_link.version = self.version
        return web_link

    def _css_select(self, document, selector):
        return document.select(selector)

    def _get_text_tag_value(self, document, selector):
        tag = self._css_select(document, selector)
        if tag:
            return Helper.encode_string(tag[0].text)

    def _get_meta_tag_value(self, document, selector):
        tag = self._css_select(document, selector)
        if tag:
            return Helper.encode_string(tag[0]['content'])

    def inspect(self):
        result = WebInspector()
        page_loader = Helper.get_page_by_url(self.url)
        if page_loader.success:
            try:
                content = page_loader.content
                document = BeautifulSoup(content)
                web_link = self._get_web_link()
                web_link.title = self._get_text_tag_value(document, 'title')
                web_link.description = self._get_meta_tag_value(document, 'meta[name=description]')
                web_link.keywords = self._get_meta_tag_value(document, 'meta[name=keywords]')
                web_link.author = self._get_meta_tag_value(document, 'meta[name=author]')
                web_link.save()
                result.success = True
                result.web_link = web_link
            except Exception as e:
                message = u"Exception on inspection url {}: {}".format(self.url, repr(e))
                result.success = False
                result.message = message
        else:
            result.success = False
            result.message = page_loader.message
        return result

