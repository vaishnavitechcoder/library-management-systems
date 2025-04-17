from odoo import http
from odoo.http import request

class Library(http.Controller):

    @http.route('/library/books/', website="True", auth="public")
    def library_book(self, **kw):
        books = request.env["library.books"].sudo().search([])
        print(books)
        return http.request.render("librarys.books_pages",{
            "books" : books
        })

    @http.route(['/book/<int:book_id>'], type='http', auth='public', website=True)
    def book_detail(self, book_id):
        book = request.env['library.books'].sudo().browse(book_id)
        return http.request.render('librarys.book_detail', {
            'book': book
        })

    @http.route(['/book/review'], type='http', auth='user', website=True, csrf=True)
    def submit_review(self, **post):
        request.env['library.review'].sudo().create({
            'book_id': int(post.get('book_id')),
            'user_id': request.uid,
            'rating': int(post.get('rating')),
            'comment': post.get('comment'),
        })
        return http.request.redirect(f'/book/{post.get("book_id")}')
