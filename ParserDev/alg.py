# Exit a parse tree produced by MiniJavaParser#pexp_aux.
def exitPexp_aux(self, ctx:MiniJavaParser.Pexp_auxContext):
    
    if ctx.getChildCount() == 2:
        self.dicionarioTipos[ctx.__hash__()] = ctx.ID().getText()    

    elif ctx.pexp_aux() != None: #se tiver um pexp_aux no final
        if ctx.LPAREN() !=None: #se tiver id. ( params? ) pexp_aux
            funcaoAux = None
            pos = 0
            
            #buscando funcao cujo identificador é ID
            while funcaoAux == None and pos < len(self.table):
                table_aux = self.table[pos]
                funcaoAux = table_aux.findFunction(ctx.ID().getText, len(self.table))
                pos = pos+1
                
            #funcaoAux é a funcao referente ao ID
            #caso ela tenha sido implementada
            if funcaoAux != None:
                name_aux = ctx.pexp_aux().getChild(1).getText() #nome do metodo ou id do pexp_aux
                class_name = funcaoAux.returnType               #tipo do retorno do metodo referente a ID
                
                ind = self.findClass(class_name) #indice da classe encontrada do retorno do ID
                
                if ind != None:  #se o tipo do retorno for uma classe                              
                    if ctx.pexp_aux().LPAREN() != None:
                        fun = self.table[ind].findFunction(name_aux) #tipo do retorno de pexp_aux
                        if fun != None:
                            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                        else:
                            print("nao existe o metodo '" + name_aux + "'. ")
                            sys.exit()                                 
                    else:
                        ident = self.table[ind].findID(name_aux) #tipo do retorno de pexp_aux
                        if ident != None :
                            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                        else:
                            print("não existe o atributo '" + name_aux + "' na classe '" + class_name + "'.)
                else:
                    print("tipo do retorno do metodo não é uma classe. Por isso não é possivel acessar metodos ou parametros")
                
                if ctx.exps() != None: # .id (exps) . pexp_aux
                    #verificação do tipo dos parametros passados para a funcao
                    listParametros =  funcaoAux.getParamsList()
                    tamList = len(listParametros)
                    paramsRecebidos = self.dicionarioTipos[ctx.exps().__hash__()]
                    tamParamsRecebidos = len(paramsRecebidos)

                    if tamParamsRecebidos == tamList:                        
                        for i in range(tamList):
                            if listParametros[i] != paramsRecebidos[i]:
                                print("Parametro '" + ctx.exps().exp(i).getText() + "'' passado pra função' " + funcaoAux.name + "'' não é do tipo " + paramsRecebidos[i] +".")                        
                            #falta verificar caso o tipo da parada seja subtipo da outra                        
                    else:
                        print("Numero de parametros passados para a função '" + funcaoAux.name + "' é incompativel.")

            else:
                print("não existe '" + ctx.pexp_aux().getChild(1).getText() + "' em '" + ctx.ID().getText() + "'.")
                sys.exit()
                  
        else: #.id . pexp_aux
            for i in range(len(self.table)):
                if(ctx.ID().getText() == self.table[i].name[0]):
                    if ctx.pexp_aux().LPAREN() != None:
                        fun = self.table[i].findFunction(ctx.pexp_aux().getChild(1).getText(),len(self.table)) #tipo do retorno de pexp_aux
                        if fun != None:
                            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                        else:
                            print("nao existe o metodo '" + name_aux + "'. ")
                            sys.exit()                                 
                    else:
                        ident = self.table[i].findID(name_aux) #tipo do retorno de pexp_aux
                        if ident != None :
                            self.dicionarioTipos[ctx.__hash__()] = self.dicionarioTipos[ctx.pexp_aux().__hash__()]
                        else:
                            print("não existe o atributo '" + name_aux + "' na classe '" + class_name + "'.)
    else:
        funcaoAux = None
        pos = 0
        
        #buscando funcao cujo identificador é ID
        while funcaoAux == None and pos < len(self.table):
            table_aux = self.table[pos]
            funcaoAux = table_aux.findFunction(ctx.ID().getText, len(self.table))
            pos = pos+1

        if funcaoAux != None:
            self.dicionarioTipos[ctx.__hash__()] = funcaoAux.returnType
            if ctx.exps() != None:  #.id(exps)
                                    #verificação do tipo dos parametros passados para a funcao
                listParametros =  funcaoAux.getParamsList()
                tamList = len(listParametros)
                paramsRecebidos = self.dicionarioTipos[ctx.exps().__hash__()]
                tamParamsRecebidos = len(paramsRecebidos)

                if tamParamsRecebidos == tamList:
                    for i in range(tamList):
                        if listParametros[i] != paramsRecebidos[i]:
                            print("Parametro '" + ctx.exps().exp(i).getText() + "'' passado pra função' " + funcaoAux.name + "'' não é do tipo " + paramsRecebidos[i] +".")                        
                        #falta verificar caso o tipo da parada seja subtipo da outra
                else:
                    print("Numero de parametros passados para a função '" + funcaoAux.name + "' é incompativel.")


        else:
            print("Retorno da fun")
