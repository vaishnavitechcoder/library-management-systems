from odoo import http
from odoo.http import request, route
import random
import json
from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal


class Library(http.Controller):

    @http.route(['/library',
                 '/library/page/<int:page>',
                 '/library/category/<model("library.category"):category>',
                 '/library/category/<model("library.category"):category>/page/<int:page>'],
                type="http", website="True", auth="public")
    def library_book(self, category=None, page=1, **kw):
        books = request.env["library.books"].sudo().search([])
        print(books)
        books_per_page = 10
        offset = (page - 1) * books_per_page
        domain = []

        if category:
            domain.append(('category_id', '=', category.id))

        books_per_page = 8
        offset = (page - 1) * books_per_page
        books = books.search(domain, limit=books_per_page, offset=offset)
        total_books = books.search_count(domain)
        total_pages = (total_books + books_per_page - 1) // books_per_page

        quotes = [
            {"text": "So many books, so little time.", "author": "Frank Zappa"},
            {"text": "A reader lives a thousand lives before he dies. The man who never reads lives only one.",
             "author": "George R.R. Martin"},
            {"text": "Books are a uniquely portable magic.", "author": "Stephen King"},
            {"text": "Reading is essential for those who seek to rise above the ordinary.", "author": "Jim Rohn"},
            {"text": "That’s the thing about books. They let you travel without moving your feet.",
             "author": "Jhumpa Lahiri"},
            {"text": "Reading is to the mind what exercise is to the body.", "author": "Joseph Addison"},
            {"text": "We read to know we are not alone.", "author": "C.S. Lewis"},
            {"text": "I have always imagined that Paradise will be a kind of library.", "author": "Jorge Luis Borges"},
            {"text": "A room without books is like a body without a soul.", "author": "Cicero"},
            {"text": "Once you learn to read, you will be forever free.", "author": "Frederick Douglass"},
            {
                "text": "Books are the carriers of civilization. Without books, history is silent, literature dumb, science crippled, thought and speculation at a standstill.",
                "author": "Barbara W. Tuchman"},
            {"text": "Reading without reflecting is like eating without digesting.", "author": "Edmund Burke"},
            {
                "text": "It is what you read when you don’t have to that determines what you will be when you can’t help it.",
                "author": "Oscar Wilde"},
            {"text": "No two persons ever read the same book.", "author": "Edmund Wilson"},
            {"text": "A book is a dream that you hold in your hands.", "author": "Neil Gaiman"},
            {"text": "You can never get a cup of tea large enough or a book long enough to suit me.",
             "author": "C.S. Lewis"},
            {"text": "The best advice I ever got was that knowledge is power and to keep reading.",
             "author": "David Bailey"},
            {"text": "I owe everything I am and everything I will ever be to books.", "author": "Gary Paulsen"},
            {
                "text": "My alma mater was books, a good library… I could spend the rest of my life reading, just satisfying my curiosity.",
                "author": "Malcolm X"},
            {"text": "Reading is a basic tool in the living of a good life.", "author": "Mortimer J. Adler"},
            {
                "text": "Reading is an act of civilization; it’s one of the greatest acts of civilization because it takes the free raw material of the mind and builds castles of possibilities.",
                "author": "Ben Okri"},
            {
                "text": "Books are the quietest and most constant of friends; they are the most accessible and wisest of counselors, and the most patient of teachers.",
                "author": "Charles W. Eliot"},
            {"text": "Many people, myself among them, feel better at the mere sight of a book.",
             "author": "Jane Smiley"},
            {"text": "Books and doors are the same thing. You open them, and you go through into another world.",
             "author": "Jeanette Winterson"},
            {"text": "Keep reading. It’s one of the most marvelous adventures that anyone can have.",
             "author": "Lloyd Alexander"},
            {"text": "The library is inhabited by spirits that come out of the pages at night.",
             "author": "Isabel Allende"},
            {"text": "When I have a little money, I buy books; and if I have any left, I buy food and clothes.",
             "author": "Desiderius Erasmus"},
            {
                "text": "Books are not made for furniture, but there is nothing else that so beautifully furnishes a house.",
                "author": "Henry Ward Beecher"},
            {"text": "There is no friend as loyal as a book.", "author": "Ernest Hemingway"},
            {
                "text": "Read. Read anything. Read the things they say are good for you, and the things they claim are junk. You’ll find what you need to find. Just read.",
                "author": "Neil Gaiman"},
            {"text": "Let us read, and let us dance; these two amusements will never do any harm to the world.",
             "author": "Voltaire"},
            {"text": "Reading is a basic tool in the living of a good life.", "author": "Joseph Addison"},
            {"text": "Books wash away from the soul the dust of everyday life.", "author": "Unknown"},
            {"text": "Reading gives us someplace to go when we have to stay where we are.", "author": "Mason Cooley"},
            {
                "text": "So often a visit to a bookshop has cheered me and reminded me that there are good things in the world.",
                "author": "Vincent Van Gogh"},
            {
                "text": "The best moments in reading are when you come across something—a thought, a feeling, a way of looking at things—which you had thought special and particular to you. And now, here it is, set down by someone else, a person you have never met, someone even who is long dead. And it is as if a hand has come out, and taken yours.",
                "author": "Alan Bennett"},
            {"text": "Books are like imprisoned souls till someone takes them down from a shelf and frees them.",
             "author": "Samuel Butler"},
            {"text": "You’re never too old, too wacky, too wild, to pick up a book and read to a child.",
             "author": "Dr. Seuss"},
            {"text": "A true friend is like a good book, the inside is better than the cover.", "author": "Anonymous"},
            {"text": "You’re never alone when you’re reading a book.", "author": "Susan Wiggs"},
            {"text": "He that loves reading has everything within his reach.", "author": "William Godwin"},
            {
                "text": "It is books that are the key to the wide world; if you can’t do anything else, read all that you can.",
                "author": "Jane Hamilton"},
            {"text": "There is more treasure in books than in all the pirate’s loot on Treasure Island.",
             "author": "Walt Disney"},
            {"text": "Good books, like good friends, are few and chosen; the more select, the more enjoyable.",
             "author": "Louisa May Alcott"},
            {"text": "You can travel the world and never leave your chair when you read a book.",
             "author": "Sherry K. Plummer"},
            {"text": "Every book is a children’s book if the kid can read!", "author": "Mitch Hed"},
        ]
        random_quote = random.choice(quotes)

        return http.request.render("librarys.book_pages", {
            "books": books,
            'current_page': page,
            'total_pages': total_pages,
            'category': category,
            'quote': random_quote,
        })

    @http.route(['/book/<int:book_id>'], type='http', auth='public', website=True)
    def book_detail(self, book_id):
        book = request.env['library.books'].sudo().browse(book_id)
        return http.request.render('librarys.book_detail', {
            'book': book
        })

    @http.route(['/book/review'], type='http', auth='user', website=True, CSRF="True")
    def submit_review(self, **post):
        request.env['library.review'].sudo().create({
            'book_id': int(post.get('book_id')),
            'user_id': request.uid,
            'rating': int(post.get('rating')),
            'comment': post.get('comment'),
        })
        return http.request.redirect(f'/book/{post.get("book_id")}')

    @http.route(['/library/publisher'], type='http', auth='user', website=True)
    def library_publisher(self, **kw):
        publisher = request.env["library.publisher"].sudo().search([])
        print(publisher)
        return http.request.render("librarys.publisher_pages", {
            "publisher": publisher
        })

    @http.route(['/library/members'], type='http', auth='user', website=True)
    def library_members(self, country_id=None, state_id=None, status=None, **kw):

        domain = []

        if country_id:
            domain.append(('country.id', '=', int(country_id)))
        if state_id:
            domain.append(('state.id', '=', int(state_id)))
        if status:
            domain.append(('status', '=', status))
        members = request.env["library.members"].sudo().search([])

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        print(members)
        return http.request.render("librarys.members_pages", {
            "members": members,
            'countries': countries,
            'states': states,
            'selected_country': int(country_id) if country_id else None,
            'selected_state': int(state_id) if state_id else None,
            'selected_status': status,
        })

    @http.route(['/library/authors'], type='http', auth='user', website=True)
    def library_author(self, **kw):
        author = request.env["library.author"].sudo().search([])
        print(author)
        return http.request.render("librarys.author_pages", {
            "author": author
        })

    @http.route('/library/borrow', type='http', auth='user', website=True)
    def library_borrow_form(self, **kw):
        books = request.env['library.books'].sudo().search([])
        magazines = request.env['library.magazine'].sudo().search([])
        return request.render("librarys.borrow_form_page", {
            "books": books,
            "magazines": magazines,
        })

    # @http.route('/library/borrow/submit', type='http', auth='user', website=True, csrf=True)
    # def submit_borrow_form(self, **post):
    #     member = request.env['library.members'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
    #     print(member)
    #     if not member:
    #         print(member)
    #         return request.redirect('/library/borrow')
    #
    #     request.env['library.borrow'].sudo().create({
    #         'members_id': member.id,
    #         'book_id': int(post.get('book_id')) if post.get('book_id') else False,
    #         'magazine': int(post.get('magazine')) if post.get('magazine') else False,
    #         'state': 'borrowed',
    #     })
    #     return request.redirect('/library/borrow/thankyou')

    @http.route('/library/borrow/submit', type='http', auth='user', website=True, csrf=True)
    def submit_borrow_form(self, **post):
        member = request.env['library.members'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if not member:
            return request.redirect('/library/borrow')

        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else False
            except ValueError:
                return False

        state = post.get('action')  # Either 'borrowed' or 'returned'

        request.env['library.borrow'].sudo().create({
            'members_id': member.id,
            'book_id': int(post.get('book_id')) if post.get('book_id') else False,
            'magazine': int(post.get('magazine')) if post.get('magazine') else False,
            'borrow_date': parse_date(post.get('borrow_date')),
            'return_date': parse_date(post.get('return_date')),
            'actual_return_date': parse_date(post.get('actual_return_date')),
            'state': state if state in ['borrowed', 'returned'] else 'draft',
        })

        return request.redirect('/library/borrow/thankyou')

    @http.route(['/library/borrow/thankyou'], type='http', auth='user', website=True)
    def library_borrow_thankyou(self, **kw):
        return http.request.render("librarys.borrow_thankyou", {})

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        borrow_count = request.env['library.borrow'].sudo().search_count([
            ('members_id.user_id', '=', request.uid)
        ])
        values['borrow_count'] = borrow_count
        return values

    @http.route(['/my/borrowed'], type='http', auth="user", website=True)
    def portal_my_borrowed_books(self, sortby='newest', filterby='all', **kwargs):

        sortings = self._borrow_books_searchbar_sortings()
        filters = self._borrow_books_searchbar_filters()

        domain = [('members_id.user_id', '=', request.env.user.id)]
        if filterby in filters:
            domain += filters[filterby]['domain']

        order = sortings.get(sortby, sortings['newest'])['order']

        borrow_records = request.env['library.borrow'].sudo().search(domain,order=order)

        return request.render("librarys.portal_borrowed_books", {
            'borrow_records': borrow_records,
            'searchbar_sortings': sortings,
            'sortby': sortby,
            'searchbar_filters': filters,
            'filterby': filterby,
            'default_url': '/my/borrowed'
        })

    def _borrow_books_searchbar_filters(self):
        return {
            'all': {'label': 'All', 'domain': []},
            'returned': {'label': 'Returned', 'domain': [('state', '=', 'returned')]},
            'borrowed': {'label': 'Borrowed', 'domain': [('state', '=', 'borrowed')]},
            'draft': {'label': 'Draft', 'domain': [('state', '=', 'draft')]},
        }

    def _borrow_books_searchbar_sortings(self):
        return {
            'newest': {'label': 'Newest', 'order': 'borrow_date desc'},
            'oldest': {'label': 'Oldest', 'order': 'borrow_date asc'},
            'book_title': {'label': 'Book Title', 'order': 'book_id.name asc'},
        }

    @http.route('/library/blog', auth='public', website=True)
    def library_books_blog(self, **kwargs):
        books = request.env['library.books'].search([])
        return request.render('librarys.library_book_list', {'books': books})

    @http.route('/library/<model("library.books"):book>', auth='public', website=True)
    def book_detail_blog(self, book, **kwargs):
        return request.render('librarys.library_book_detail', {'book': book})

    @route('/test', type='json', auth='user', methods=['POST'], website=True)
    def get_books(self, **kwargs):
        # Fetch all available books
        books = request.env['library.borrow'].search([])
        print(books)
        return books

    @route('/custom_sidebar', auth='public',website=True)
    def custom_sidebar(self, **kwargs):
        return request.render('librarys.custom_sidebar')
