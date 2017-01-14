# gets fullpath cause executable doesnt seem to have any __file__ property
import os.path,os

fullpath = os.path.abspath(__file__)
# print fullpath