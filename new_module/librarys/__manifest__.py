{
    "name" : "librery management system",
    "version":"1.0",
    "author": "Vaishnavi patil",
    "sequence":10,
    "license":"LGPL-3",
    "application":True,
    "installable":True,
    "depends": [
            "base","mail"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/book_reservation_view.xml",
        "data/author_view.xml",
        "views/books_view.xml",
        "views/members_view.xml",
        "views/borrow_view.xml",
        "views/category_view.xml",
        "views/fines_view.xml",
        "views/authors_view.xml",
        "views/magzine_view.xml",
        "views/settings_view.xml",
    ],
}