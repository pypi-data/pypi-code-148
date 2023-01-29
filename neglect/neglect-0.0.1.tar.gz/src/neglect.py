
import os

def neglect(test):
    ci, afsp = 0, 3
    f2=open("test1.py",'w')
    f1=open(test,'r')
    f2.write("import os, sys\ntry:\n")
    on=0
    y=0
    count=0
    ex=[]
    for i in f1:

      count+=1
      f2.write("\t")
      if i.count("input") == 0 and i.count("print") == 0:

        if i.count("except") !=0:
         y+=1
         ex.append(count-1)
         sp=""
         p=str(i)
         l=len(p)-len(p.lstrip())
         for j in range(l):
            sp+=" "

         s=i+sp+"\t\texc_type, exc_obj, exc_tb=sys.exc_info()\n"+sp+"\t\tfname=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]\n"+sp+"\t\tf3=open(\"error.txt\",'w')\n"+sp+"\t\tf3.write(str(exc_tb.tb_lineno))\n"+sp+"\t\tf3.close()\n"
         f2.write(s)
         on=1

      #f2.write("\nexcept Exception as e:\n\texc_type, exc_obj, exc_tb=sys.exc_info()\n\tfname=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]\n\tf3=open(\"error.txt\",'w')\n\tf3.write(str(exc_tb.tb_lineno))\n\tf3.close()\n\t")
        else:
            if on ==0:
             f2.write(i)

            else:

                i="\t"+sp+i.lstrip()
                f2.write(i)
                on=0
      else:


          j="#"+i
          f2.write(j)



    f2.write("\nexcept Exception as e:\n\texc_type, exc_obj, exc_tb=sys.exc_info()\n\tfname=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]\n\tf3=open(\"error.txt\",'w')\n\tf3.write(str(exc_tb.tb_lineno))\n\tf3.close()\n\t")
    f1.close()
    f2.close()

    os.system("python test1.py")
    if os.path.isfile("error.txt") == True:
        f3=open("error.txt",'r')
    else:
        os.remove('test1.py')
        os.system('python test.py')

        exit(0)


    f5=open("../test.py", 'r')
    data=f5.readlines()


    for i in f3:

        if i == " ":
            f3.close()
            os.remove('error.txt')
            os.remove('test1.py')
            os.system('python test.py')
            exit(0)

        for t in range(len(ex)):

          if ex[t]>=int(i):

            afsp=3
          else:
            afsp+=5

        if ex!=[]:
         ex.pop(0)
        sp1 = ""

        p1 = str(data[int(i)-afsp])
        l1 = len(p1) - len(p1.lstrip())
        for j in range(l1):
            sp1 += " "
        data[int(i) - afsp]=data[int(i)-afsp].replace("\n"," ")
        data[int(i)-afsp]=    sp1+  "#"+data[int(i)-afsp] +"  -----------  Error occurs in this line\n"


    f5.close()
    f4=open("../test.py", 'w')
    f4.writelines(data)
    f4.close()
    f3.close()
    f7=open("error.txt",'w')
    f7.write(" ")
    f7.close()
    os.system('python neglect.py')

