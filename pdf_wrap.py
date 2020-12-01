import os
import sys
import time

cmd = "python3 ~/Desktop/pdfmaker/pdfmaker.py {} {}"

folderPath = sys.argv[1]
os.chdir(folderPath)
os.system("mkdir original processed ongoing")
for pdf in [i for i in os.listdir(folderPath) if i.endswith(".pdf")]:
    print(pdf)
    os.chdir(folderPath)
    #print(f"mv {folderPath}/{pdf} {folderPath}/ongoing")
    os.system(f"mv {folderPath}/{pdf} {folderPath}/ongoing")
    os.system(cmd.format(f"{folderPath}/ongoing", f"{pdf[:-4]}-processed.pdf"))
    os.system(f"mv {folderPath}/ongoing/{pdf} original")
    os.system(f"mv {folderPath}/ongoing/{pdf[:-4]}-processed.pdf processed")

time.sleep(1)
os.system("rmdir ongoing")
print("complete")






