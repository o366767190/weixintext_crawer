#coding:utf-8
'''
Created on 2017年6月28日

@author: Shinelon
'''
import threading
class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(10):
            print('我是线程A')

class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(10):
            print('我是线程B')
            
t1=A()

t1.start()

t2=B()
t2.start()