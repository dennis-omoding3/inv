class New_stock:
    def __init__(self,stock,sale):
        self.stock=stock
        self.sale=sale

    def new_stock(self):
        new = self.stock - self.sale
        return new

x = New_stock(1000, 200)
# print(x.new_stock())