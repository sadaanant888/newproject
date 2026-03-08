# B-TYPE
    if k[0] in b:
        # eg:- beq rs1,rs2, imm[12:1]
        ans=""
        num=k[3]                          ## k[3] is imm
        bin_imm=0,x=1                     ## bin_imm will store binary of immediate. Negative immediate not handled. 
        while(num!=0):
            rem=num/2
            bin_imm=bin_imm+rem*x
            num=num/2
            x*=10
        bin_imm=str(bin_imm)
        bin_imm=bin_imm.rjust(16,'0')

        imm_12__10_5=bin_imm[-13]+bin_imm[-11:-5]           #imm_12__10_5= imm[12|10:5]= imm[12]+imm[10:5]

        ans+=imm_12__10_5+ " "           ## ans= imm[12|10:5]
        
        if k[2] in registers:
            ans+=registers[k[2]]         ## ans= imm[12|10:5]+ rs2
        if k[1] in registers:
            ans+=registers[k[1]]         ## ans= imm[12|10:5]+ rs2 + rs1
        if k[0] in instruction:
            ans+=instruction[k[0]][0]    ## ans= imm[12|10:5]+ rs2 + rs1+ funct3
        
        imm_4_1__11=bin_imm[-5:-1]+ bin_imm[-12]    #imm_4_1__11= imm[4:1|11]= imm[4:1]+imm[11]
        ans+=imm_4_1__11+ " "            ## ans= imm[12|10:5]+ rs2 + rs1+ funct3+ imm[4:1|11]

        if k[0] in instruction:
            ans+=instruction[k[0]][1]    ## ans= imm[12|10:5]+ rs2 + rs1+ funct3+ imm[4:1|11]+ opcode