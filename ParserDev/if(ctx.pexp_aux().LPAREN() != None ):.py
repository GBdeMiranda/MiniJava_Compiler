if(ctx.pexp_aux().LPAREN() != None ):
    funcaoAux = self.table[i].findFunction(ctx.pexp_aux().getChild(1).getText(), len(self.table))
    if funcaoAux != None:
        self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
    else:
        print("Não existe o método usado")
        linha = ctx.getChild(0).symbol.line
        coluna = ctx.getChild(0).symbol.column
        print("Erro na linha "+ linha + " coluna " + coluna +" ." )                            
        sys.exit()
    break
else:
    idAux = self.table[i].findID(ctx.pexp_aux().getChild(1).getText())
    if idAux != None:
        self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
    else:
        print("Não existe o identificador usado")
        linha = ctx.getChild(0).symbol.line
        coluna = ctx.getChild(0).symbol.column
        print("Erro na linha "+ linha + " coluna " + coluna +" ." )                            
        sys.exit()
    break
