import os
import sys

# Get the absolute path of the project root directory
#  C:\Users\shafi\OneDrive\Desktop\Codebasics\python\projects\expense_tracking_system adding this into system path so test_db_helper can find every files

project_root = os.path.join(os.path.dirname(__file__), '..')
print("PROJECT ROOT: ",project_root)
sys.path.insert(0, project_root)
print(sys.path)