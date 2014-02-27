#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'shine'

class car_bit:
    def sound(self):
        print "car..."

class bigcar(car_bit):
    pass

def main():
    a = car_bit()
    a.sound()
    a = bigcar()
    a.sound()

if __name__ == '__main__':
    main()