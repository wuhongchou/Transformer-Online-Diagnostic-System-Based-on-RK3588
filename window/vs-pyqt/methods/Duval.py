

'''
Input:
%------
%The input is the gas concentrations stored in a vector named 'ppms' 
%and stored again in the following nine variables:
%h2=ppms(1);ch4=ppms(2);c2h6=ppms(3);c2h4=ppms(4);c2h2=ppms(5);
%co=ppms(6);co2=ppms(7);n2=ppms(8);o2=ppms(9);
%Note that unused gas concentrations take the value -1

% Analysis
%---------
% Implement your fault diagnosis method here 

%Output:
%-------
% set 'Diagnosis' variable to a number between 0 and 7 representing the 
% fault code resulting from your analysis method 
% {0=NF,1=PD,2=D1,3=D2,4=T1,5=T2,6=T3,7=UD}
'''
class Duvalclass:
    def __init__(self, h2, ch4,c2h6,c2h4,c2h2):
        self.h2 = h2
        self.ch4 = ch4
        self.c2h6=c2h6
        self.c2h4=c2h4
        self.c2h2=c2h2

    def Duvalrun(self):
     a1=(self.ch4/(self.ch4+self.c2h4+self.c2h2))*100 
     a2=(self.c2h4/(self.ch4+self.c2h4+self.c2h2))*100
     a3=(self.c2h2/(self.ch4+self.c2h4+self.c2h2))*100
     
     result=[]
     for i in range(len(a1)):
        R1=a1[i]
        R2=a2[i]
        R3=a3[i]
        if R1>=98 and R2<=2  and R3<=2:
         Diagnosis=1
        elif R3<=4 and R2>=20 and R2<=50 and R1<=80 and R1>=46:
         Diagnosis=5
        elif R3<=4  and R2<=20 and R1>=76 and R1<=98:
         Diagnosis=4
        elif R3>=0 and R2<=23:
         Diagnosis=2
        elif R3<=15 and  R2>=50 and R1<=50:
         Diagnosis=6
        elif  R3<=79  and R3>=13 and R2<=77:
         Diagnosis=3
        elif R3<=29 and R3>=4 and R2<=85:
         Diagnosis=3
        else:
         Diagnosis=7

        result.append(Diagnosis)
     return result

     
    


