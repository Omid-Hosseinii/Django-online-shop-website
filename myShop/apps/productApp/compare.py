
# #-----------------------------------------------------------------------------------------------------------------------
class CompareProduct:
    def __init__(self,request):
        self.session = request.session
        compare_product=self.session.get('compare_product')
        if not compare_product:
            compare_product=self.session['compare_product']=[]
        self.compare_product=compare_product 
        self.count=len(self.compare_product)  
        
    def __iter__(self):
        compare_product=self.compare_product.copy()
        for item in compare_product:
            yield item
            
    def add_to_compare_list(self,productId):
        productId=int(productId)
        if productId not in self.compare_product:
            self.compare_product.append(productId)
        self.count=len(self.compare_product)
        self.session.modified=True
        
    def remove_from_compare_list(self,productId):
        productId=int(productId)
        self.compare_product.remove(productId)
        self.count=len(self.compare_product)
        self.session.modified=True
        
    def clear_compare_list(self):
        del self.session['compare_product']
        self.session.modified=True    
               
                     