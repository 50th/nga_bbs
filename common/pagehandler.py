class Pager(object):
    def __init__(self, page, data_count, page_url, page_per=10):
        self.page = page
        self.data_count = data_count
        self.page_url = page_url
        self.page_per = page_per
        self.page_count = data_count // page_per if data_count % page_per == 0 else data_count // page_per + 1
        if self.page + 2 > self.page_count:
            self.start_page = self.page_count-4 if self.page_count-4 > 0 else 1
        else:
            self.start_page = page - 2 if page > 2 else 1
        if self.page - 2 <= 0:
            self.end_page = 5 if self.page_count >= 5 else self.page_count
        else:
            self.end_page = self.page_count - 1 if page < self.page_count-2 else self.page_count

    def get_page_bar(self):

        """<td><a>1</a></td><td><a class="active">1</a></td><td><a>1</a></td><td><a>1</a></td><td><a>1</a></td>
        """

        page_bar = """
            <div class="page-bar">
                <table>
                    <tbody>
                        <tr>   
        """

        if self.page > 1:
            page_bar += """<td><a href="%s?page=%d">前页</a></td>""" % (self.page_url, self.page-1)

        for i in range(self.start_page, self.end_page + 1):
            if i == self.page:
                page_bar += """<td><a class='active' href="%s?page=%d">%d</a></td>""" % (self.page_url, i, i)
            else:
                page_bar += """<td><a href="%s?page=%d">%d</a></td>""" % (self.page_url, i, i)
        if self.page < self.page_count:
            page_bar += """<td><a href="%s?page=%d">后页</a></td>""" % (self.page_url, self.page+1)
        page_bar += """
                        </tr>
                    </tbody>
                </table>
            </div>
        """
        return page_bar

    @property
    def start_index(self):
        return (self.page-1) * self.page_per

    @property
    def end_index(self):
        return self.page * self.page_per
