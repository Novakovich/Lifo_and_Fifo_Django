This project is developed on the basis of the experience gained during the training on Python Developer and contains the basic principles and knowledge of designing on Django framework. As a basis for the idea was a site for making and giving donations depending on the location and characteristics of donations, as well as developed the ability to communicate in chat.
Main knowledge and skills used in development:
- Migrated from SQLite3 to PostgreSQL.
- added sessions for selecting city to get donation.
- used select_for_update to lock a transaction.
- used Forms and Formsets, expanded model descriptions with Meta Class: Abstract and Proxy, constraints (F and Q).
- added donation receipt date, donation description, donation image, etc.  
- made a signal if storage is full, and made "disabled" button to have no ability to add to overflowing storage.
- changed the id to uuid by migrations.
- Ability to find donation by donation name or by criteria.
- built-in admin panel with all features for data manipulation (sorting, changing fields, immutable fields, actions, Search fields by uuid)
- worked with DjangoRestFramework API and Postman, created serializers and connected urls.py
- enabled login and logout
- used celery and rabbitMQ to notify user about registration.  
- The latest: added context_processor, select_related, debug_toolbar and chat.
In the visual design I tried to work out the HTML with Bootstrap5, crispy_forms, added header for all pages, connected STATIC FILES and MEDIA FILES and other features.
