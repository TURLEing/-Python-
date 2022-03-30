class machine :
    def __init__(self, Statement, Env) :  
        self.Statement, self.Env = Statement, Env
    def run(self) :
        while self.Statement.reduciable : # 若当前表达式可进一步规约
            print(self.Statement)  
            for i, j in self.Env.items():
                print("{key} : {value}".format(key=i, value=j), end='; ')
            print()
            print()
            self.Statement, self.Env = self.Statement.reduce(self.Env)  
            # 由于语句的存在会修改环境，每次规约都应该返回环境
        print(self.Statement)
        if self.Env != None :
            for i, j in self.Env.items():
                print("{key} : {value}".format(key=i, value=j), end='; ')
        print()

# 值
class number :
    def __init__(self, val, reduciable = 0) :  # number 规约值缺省为 0
        self.val, self.reduciable = val, 0
    def __str__(self) : return str(self.val)

class boolean :
    def __init__(self, val, reduciable=0):  # boolean 规约值缺省为 0
        self.val, self.reduciable = val, 0
    def __str__(self) : return ("TRUE" if self.val==1 else "FALSE")

class variable :
    def __init__(self, name, reduciable=1) :
        self.name, self.reduciable = name, 1
    def __str__(self) : return str(self.name)
    def reduce(self, Env) : return Env[self.name]

# 运算
class Add :
    def __init__(self, left, right, reduciable = 1) :  # 运算的规约值默认为 1
        self.left, self.right, self.reduciable = left, right, 1
    def __str__(self):
        return str(self.left) + "+" + str(self.right)
    def reduce(self, Env) :  # 优先往右规约，再规约左
        if self.left.reduciable :
            return Add(self.left.reduce(Env), self.right)
        elif self.right.reduciable :
            return Add(self.left, self.right.reduce(Env))
        else : return number(self.left.val + self.right.val)

class Multi :
    def __init__(self, left, right, reduciable = 1) :
        self.left, self.right, self.reduciable = left, right, 1
    def __str__(self) :
        return str(self.left) + "*" + str(self.right)
    def reduce(self, Env) :  # 规约算法同理
        if self.left.reduciable :
            return Multi(self.left.reduce(Env), self.right)
        elif self.right.reduciable :
            return Multi(self.left, self.right.reduce(Env))
        else : return number(self.left.val * self.right.val)

class Less :
    def __init__(self, left, right, reduciable = 1) :
        self.left, self.right, self.reduciable = left, right, 1
    def __str__(self) :
        return str(self.left) + "<" + str(self.right)
    def reduce(self, Env) :  # 规约算法同理
        if self.left.reduciable :
            return Less(self.left.reduce(Env), self.right)
        elif self.right.reduciable :
            return Less(self.left, self.right.reduce(Env))
        else : return boolean(self.left.val < self.right.val)
        
# 语句
class Do_nothing :
    def __init__(self, reduciable=0) : self.reduciable = 0
    def __str__(self) : return "Do-nothing"

class Assign : 
    def __init__(self, name, Expression, reduciable = 1) :
        self.name, self.Expression, self.reduciable = name, Expression, 1
    def __str__(self) : 
        return str(self.name) + " = " + str(self.Expression)
    def reduce(self, Env) :
        if self.Expression.reduciable :
            return [Assign(self.name, self.Expression.reduce(Env)), Env]
        else :
            Env.update( {str(self.name) : self.Expression} )
            return [Do_nothing(), Env]
            # 赋值语句进行后更新环境

class IfCase :
    def __init__(self, condition, state1, state2, reduciable = 1) :
        self.condition, self.state1, self.state2, self.reduciable = condition, state1, state2, 1
    def __str__(self) :
        return "If ("+str(self.condition)+") : {"+str(self.state1)+"} else {"+str(self.state2)+"}"
    def reduce(self, Env) :
        if self.condition.reduciable : 
            return IfCase(self.condition.reduce(Env), self.state1, self.state2), Env
        # 若条件可规约
        else : 
            if self.condition.val == 1 : return self.state1, Env
            else : return self.state2, Env

class Seq :
    def __init__(self, state1, state2, reduciable=1) :
        self.state1, self.state2, self.reduciable = state1, state2, 1
    def __str__(self) :
        return str(self.state1)+", "+str(self.state2)
    def reduce(self, Env) :
        if (self.state1.reduciable) : 
            new_state1, new_env = self.state1.reduce(Env)
            return Seq(new_state1, self.state2), new_env
        else : return self.state2, Env

class While :
    def __init__(self, condition, state, reduciable=1) :
        self.condition, self.state, self.reduciable = condition, state, 1
    def __str__(self):
        return "while ("+str(self.condition)+") : {"+str(self.state)+" } "
    def reduce(self, Env):
        return IfCase(self.condition, Seq(self.state, self), Do_nothing()), Env

def main() :
    print("OK")
    Statement = While(Less(variable("x"), number(5)), 
                      Seq(Assign(variable("y"), Add(variable("y"), variable("x"))), 
                      Assign(variable("x"), Add(variable("x"), number(1)))))
    Env = {"x": number(1), "y": number(0)}
    machine(Statement, Env).run()

main()