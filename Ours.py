import time
import HIBE
import OTS


def Setup(max_level):

    max_level_HIBE = 2 * max_level + 2
    HIBE_System_para, HIBE_PP, HIBE_MK = HIBE.Setup(max_level_HIBE)
    
    return HIBE_System_para, HIBE_PP, HIBE_MK


def SkGen(System_para, PP, MK, ID_string):

    len_of_ID = len(ID_string)
    Enc_ID_string = ['Enc'] + ID_string

    Trace_ID_string = ['Trace']
    for i in range(len_of_ID):
        Trace_ID_string.append(ID_string[i])
        Trace_ID_string += ['bot']

    Sk_1_I = HIBE.SkGen(System_para, PP, MK, Enc_ID_string)
    Sk_2_I = HIBE.SkGen(System_para, PP, MK, Trace_ID_string)
    Sk_ID = {'Sk_1_I': Sk_1_I, 'Sk_2_I': Sk_2_I}


    return Sk_ID


def SkDel(System_para, PP, Sk_ID, Del_ID_string):

    ID_string = Sk_ID['Sk_2_I']['ID_string']
    len_of_Del_ID = len(Del_ID_string)
    Del_Enc_ID_string = ['Enc'] + Del_ID_string
    Del_Trace_ID_string = ID_string + [Del_ID_string[-1]]
    

    Sk_Del_1_I = HIBE.SkDel(System_para, PP, Sk_ID['Sk_1_I'], Del_Enc_ID_string)

    tmp_Sk_Del_2_I = HIBE.SkDel(System_para, PP, Sk_ID['Sk_2_I'],Del_Trace_ID_string)

    Del_Trace_ID_string += ['bot']
    Sk_Del_2_I = HIBE.SkDel(System_para, PP, tmp_Sk_Del_2_I, Del_Trace_ID_string)

    Sk_Del_ID = {'Sk_1_I': Sk_Del_1_I, 'Sk_2_I': Sk_Del_2_I}
    return Sk_Del_ID

def Enc(System_para, PP, receiver_ID_string, plaintext):

    len_of_receiver_ID_string = len(receiver_ID_string)
    Osk, Ovk = OTS.Setup()
    
    serialize_Ovk = OTS.Serialize_Ovk(Ovk)
    Enc_ID_string = ['Enc'] + receiver_ID_string + [serialize_Ovk]

    Enc_key_1, Enc_message_1 = HIBE.Enc(System_para, PP, Enc_ID_string, plaintext)


    Trace_ID_string = ['Trace']
    for i in range(len_of_receiver_ID_string):
        Trace_ID_string.append(receiver_ID_string[i])
        Trace_ID_string += ['bot']
    Trace_ID_string += [serialize_Ovk]
    serialize_CT_1 = HIBE.Serialize_CT(System_para, Enc_key_1, Enc_message_1)

    Enc_key_2, Enc_message_2 = HIBE.Enc(System_para, PP, Trace_ID_string, serialize_CT_1)

    serialize_CT_2 = HIBE.Serialize_CT(System_para, Enc_key_2, Enc_message_2)

    sigma = OTS.Sign(Osk, serialize_CT_1 + serialize_CT_2)

    CT = {'sigma': sigma, 'Ovk': Ovk, 'Enc_key_2': Enc_key_2, 'Enc_message_2': Enc_message_2}
    return CT

def Dec(System_para, PP, receiver_Sk, CT):

    Sk_1_I = receiver_Sk['Sk_1_I']
    Enc_ID_string = Sk_1_I['ID_string']

    
    Sk_2_I = receiver_Sk['Sk_2_I']
    Trace_ID_string = Sk_2_I['ID_string']

    Ovk = CT['Ovk']
    sigma = CT['sigma']

    serialize_Ovk = OTS.Serialize_Ovk(Ovk)

    Del_Trace_ID_string = Trace_ID_string + [serialize_Ovk]
    Sk_Del_2_I = HIBE.SkDel(System_para, PP, Sk_2_I, Del_Trace_ID_string)

    serialize_CT_1 = HIBE.Dec(System_para, PP, Sk_Del_2_I, CT['Enc_key_2'], CT['Enc_message_2'])

    serialize_CT_2 = HIBE.Serialize_CT(System_para, CT['Enc_key_2'], CT['Enc_message_2'])

    Vrfy_CT_1, Enc_key_1, Enc_message_1 = HIBE.De_serialize_CT(System_para, serialize_CT_1)

    
    result = OTS.Vrfy(Ovk, sigma, Vrfy_CT_1 + serialize_CT_2)


    Del_Enc_ID_string = Enc_ID_string + [serialize_Ovk]
    
    Sk_Del_1_I = HIBE.SkDel(System_para, PP, Sk_1_I, Del_Enc_ID_string)

    
    result = HIBE.Dec(System_para, PP, Sk_Del_1_I, Enc_key_1, Enc_message_1)

    return result

def TkGen(System_para, PP, MK, ID_string):

    len_of_ID = len(ID_string)

    Trace_ID_string = ['Trace']
    for i in range(len_of_ID):
        Trace_ID_string.append(ID_string[i])
        Trace_ID_string += ['bot']
    Trace_ID_string = Trace_ID_string[:-1]
    Tk_ID = HIBE.SkGen(System_para, PP, MK, Trace_ID_string)

    return Tk_ID

# consider sk_id to tk_id'
def TkDel(System_para, PP, Sk_ID, Del_ID_string):

    ID_string = Sk_ID['Sk_2_I']['ID_string']
    Del_Trace_ID_string = ID_string + [Del_ID_string[-1]]
    
    Tk_Del_ID = HIBE.SkDel(System_para, PP, Sk_ID['Sk_2_I'], Del_Trace_ID_string)

    return Tk_Del_ID

def TkVer(System_para, PP, tracer_Sk, CT):

    Tk_ID = tracer_Sk
    
    Trace_ID_string = Tk_ID['ID_string']

    tmp_Del_Trace_ID_string = Trace_ID_string + ['bot']
    tmp_Tk_Del_I = HIBE.SkDel(System_para, PP, Tk_ID, tmp_Del_Trace_ID_string)

    Ovk = CT['Ovk']
    serialize_Ovk = OTS.Serialize_Ovk(Ovk)

    Del_Trace_ID_string = tmp_Del_Trace_ID_string + [serialize_Ovk]
    Tk_Del_I = HIBE.SkDel(System_para, PP, tmp_Tk_Del_I, Del_Trace_ID_string)

    serialize_CT_1 = HIBE.Dec(System_para, PP, Tk_Del_I, CT['Enc_key_2'], CT['Enc_message_2'])
    
    serialize_CT_2 = HIBE.Serialize_CT(System_para, CT['Enc_key_2'], CT['Enc_message_2'])
    sigma = CT['sigma']


    Vrfy_CT_1, Enc_key_1, Enc_message_1 = HIBE.De_serialize_CT(System_para, serialize_CT_1)
    result = OTS.Vrfy(Ovk, sigma, Vrfy_CT_1 + serialize_CT_2)

    return result

if __name__== "__main__" :

    plaintext = b'Hello'
    max_level = 5

    start1 = time.time()
    System_para, PP, MK = Setup(max_level)
    end1 = time.time()


    ID_string = ["Alice", "Bob", "Cindy"]

    start2 = time.time()
    Sk_ID = SkGen(System_para, PP, MK, ID_string)
    end2 = time.time()

    Del_ID_string = ["Alice", "Bob", "Cindy", "Davis"]

    start3 = time.time()
    Sk_Del_ID = SkDel(System_para, PP, Sk_ID, Del_ID_string)
    end3 = time.time()

    receiver_ID_string = Del_ID_string

    start4 = time.time()
    CT = Enc(System_para, PP, receiver_ID_string, plaintext)
    receiver_Sk = Sk_Del_ID
    end4 = time.time()

    start5 = time.time()
    result1 = Dec(System_para, PP, receiver_Sk, CT)
    end5 = time.time()

    start6 = time.time()
    Tk_ID = TkGen(System_para, PP, MK, ID_string)
    end6 = time.time()

    # delegate sk_ID to tk_ID'
    start7 = time.time()
    Tk_Del_ID = TkDel(System_para, PP, Sk_ID, Del_ID_string)
    tracer_Tk = Tk_ID
    end7 = time.time()

    start8 = time.time()
    result2 = TkVer(System_para, PP, Tk_Del_ID, CT)
    end8 = time.time()

    print("Setup:%f s" % (end1 - start1))
    print("SkGen:%f s" % (end2 - start2))
    print("SkDel:%f s" % (end3 - start3))
    print("Enc:%f s" % (end4 - start4))
    print("Dec:%f s" % (end5 - start5))
    print("TkGen:%f s" % (end6 - start6))
    print("TkDel:%f s" % (end7 - start7))
    print("TkVer:%f s" % (end8 - start8))
