django-template
===============

Very base template project for Django applications.

Django version: 1.7.3

# Features

**Pre configured Python/Django features:**

- Advanced page and data cache examples
- Using of HTML minifiers and assets compressions
- Database optimised Model examples
- Robots.txt and dynamic generation of sitemaps (sitemap.xml, sitemap-website.xml, sitemap-cart.xml)
- Advanced usage of Class Based Views with custom pagination (which additionally passes all request GET parameters to view, it might be useful for custom filter)
- Data compression (with installed security debreach package)
- Localization
- Custom user authentication with user profile
- Multiple form support
- Model history and reversion (possibility to back to old versions of the model)
- Management commands for initial configuration
- Customized Django Suit based administration
- Pre configured specific folders of Django application (fixtures, media, static, etc.)
- Email subscription
- Contact and Application database
- Using thumbnail for images
- Slider
- Logging

**Pre configured 3rd party packages:**

- REST Framework
- Import Export (Import and Export to and from most popular file formats such as xml, csv, etc.)
- CKEditor (also configured to support file upload)
- Django Select2 (Auto select for administration)
- Easy Thumbnails
- Blog application
    - Widgets
    - Static pages
    - Posts
    - Post categories
    - Slider
    - Beep (simple twitter like model logic)
    - Blog API

# Install

To install Django Skeleton on your machine run following commands:

Clone the project

    git clone https://github.com/KenanBek/django-skeleton.git
    cd django-skeleton

Create virtual environment and install requirements

    virtualenv env
    .\env\Scripts\activate
    pip install -r requirements.txt

Initialize and run the application

    cd app
    python manage.py init
    python manage.py runserver

"python manage.py init" command will ask you to set password for administration user.

Visit **http://localhost:8000** for website, **http://localhost:8000/admin** for administration.

# Recommendations

Configure following things if you are going to use this skeleton on your projects:

- Configure django sites (enter correct name and address for the site)
- Configure application settings (settings.py)
- Configure robots.txt and sitemaps

# License

Licensed under GNU GPL v3.0

