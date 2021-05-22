class Category:
  
  def __init__(self, nome):
    self.nome = nome
    self.ledger = list()

  def __str__(self):
    title = f"{self.nome:*^30}\n"
    items = ""
    total = 0
    for item in self.ledger:
      items += f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}" + "\n"
      total += item['amount']
    output = title + items + "Total: " + str(total)
    return output 

  ###################
  def deposit(self, quantidade, descricao=""):
    deposito = dict()
    deposito["amount"] = quantidade
    deposito["description"] = descricao
    self.ledger.append(deposito)
  
  def withdraw(self, quantidade, descricao=""):
    tem_dinheiro = self.check_funds(quantidade)
    if tem_dinheiro:
      saque = dict()
      saque["amount"] = -quantidade
      saque["description"] = descricao
      self.ledger.append(saque)
      return True
    else:
      return False

  def transfer(self, quantidade, pnome):
    nome_produto = pnome.nome
    origem = self.withdraw(quantidade, "Transfer to {}".format(nome_produto))
    pnome.deposit(quantidade, "Transfer from {}".format(self.nome))
    return True if origem else False 

  def get_balance(self):
    return sum(item['amount'] for item in self.ledger)

  def check_funds(self, quantidade):
    return self.get_balance() >= quantidade
  ###################
  
  def get_withdrawls(self):
          total = 0
          for item in self.ledger:
              if item["amount"] < 0:
                  total+= item["amount"]
          return total

def truncate(n):
    multiplier = 10
    return int(n * multiplier) / multiplier

def getTotals(categories):
    total = 0
    breakdown = []
    for category in categories:
        total += category.get_withdrawls()
        breakdown.append(category.get_withdrawls())
    
    rounded = list(map(lambda x: truncate(x/total), breakdown))
    return rounded

def create_spend_chart(categories):
    res = "Percentage spent by category\n"
    i = 100
    totals = getTotals(categories)
    while i >= 0:
        cat_spaces = " "
        for total in totals:
            if total * 100 >= i:
                cat_spaces += "o  "
                #print(categories[totals.index(total)].name)
            else:
                cat_spaces += "   "
        res+= str(i).rjust(3) + "|" + cat_spaces + ("\n")
        i-=10
    
    dashes = "-" + "---"*len(categories)
    names = []
    x_axis = ""
    for category in categories:
        names.append(category.nome)

    maxi = max(names, key=len)

    for x in range(len(maxi)):
        nameStr = '     '
        for name in names:
            if x >= len(name):
                nameStr += "   "
            else:
                nameStr += name[x] + "  "
        nameStr += '\n'
        x_axis += nameStr

    res+= dashes.rjust(len(dashes)+4) + "\n" + x_axis
    return res
