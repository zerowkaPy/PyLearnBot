page_num = 4
rows_on_page = 2
rest = 0
pages = {}
buttons = ['1', '2', '3', '4', '5', '6','7', '8']

for page in range(page_num):
    page +=1
    pages[str(page)] = [button for button in buttons[:rows_on_page]]
    buttons = buttons[rows_on_page:]
    last_page = page

if rest:
    pages[str(last_page+1)] = [button for button in buttons]

pages_prop = {}



if rest:
    fin_page = page_num+1
else:
    fin_page= page_num


for page in range(page_num):
    page+=1
    if page == 1:
        pages_prop[str(page)] = "n"
    elif page_num - page == 0 and rest:
        pages_prop[str(page)] = "bn"
        pages_prop[str(page+1)] = "b"
    elif page_num - page == 0:
        pages_prop[str(page)] = "b"
    else:
        pages_prop[str(page)] = "bn"

for page in pages_prop.items():
    if page[1] == 'bn':
        print("bn")

class a:
    def __init__(self):
        self.b = 10
    def get_b(self):
        b = self.b
        b-=1
        print(b)
        print(self.b)

c = a()
c.get_b()

