from charm.toolbox.pairinggroup import (
    PairingGroup,
    ZR,
    G1,
    G2,
    GT,
    pair,
    extract_key,
)
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
import time

group = PairingGroup("MNT159")


def Setup(max_level):

    g = group.random(G1)
    hat_g = group.random(G2)
    v = group.random(ZR)
    phi_1 = group.random(ZR)
    phi_2 = group.random(ZR)

    tau = phi_1 + v * phi_2

    y_h = group.random(ZR)

    for i in range(1, max_level + 1):
        exec(f"y_u_{i} = group.random(ZR)")

    y_w = group.random(ZR)
    alpha = group.random(ZR)
    h = g**y_h
    hat_h = hat_g**y_h

    for i in range(1, max_level + 1):
        exec(f"u_{i} = g ** y_u_{i}")
        exec(f"hat_u_{i} = hat_g ** y_u_{i}")
        exec(f"u_v_{i} = u_{i} ** v")
        exec(f"u_minus_tau_{i} = u_{i} ** -tau")

    hat_w = hat_g**y_w
    hat_w_phi_1 = hat_w**phi_1
    hat_w_phi_2 = hat_w**phi_2
    Sigma = pair(g, hat_g) ** alpha

    MK = {"hat_g": hat_g, "hat_g_alpha": hat_g**alpha, "hat_h": hat_h}
    for i in range(1, max_level + 1):
        MK["hat_u_" + str(i)] = eval("hat_u_" + str(i))

    PP = {
        "g": g,
        "g_v": g**v,
        "g_minus_tau": g**-tau,
        "h": h,
        "h_v": h**v,
        "h_minus_tau": h**-tau,
        "hat_w": hat_w,
        "hat_w_phi_1": hat_w_phi_1,
        "hat_w_phi_2": hat_w_phi_2,
        "Sigma": Sigma,
    }

    for i in range(1, max_level + 1):
        PP["u_" + str(i)] = eval("u_" + str(i))
        PP["u_v_" + str(i)] = eval("u_v_" + str(i))
        PP["u_minus_tau_" + str(i)] = eval("u_minus_tau_" + str(i))

    System_para = {"max_level": max_level}

    return System_para, PP, MK


def SkGen(System_para, PP, MK, ID_string):
    max_level = System_para["max_level"]

    ID = [group.hash(i) for i in ID_string]
    len_of_ID = len(ID_string)

    r_1 = group.random(ZR)
    c_1 = group.random(ZR)
    c_2 = group.random(ZR)

    for i in range(len_of_ID + 1, max_level + 1):
        exec(f"c_3_{i} = group.random(ZR)")

    tmp = group.init(G2)
    for i in range(1, len_of_ID + 1):
        tmp += MK["hat_u_" + str(i)] ** ID[i - 1]
    tmp_2 = (MK["hat_h"] * tmp) ** r_1
    K_1_1 = MK["hat_g_alpha"] * tmp_2 * (PP["hat_w_phi_1"] ** c_1)

    K_1_2 = PP["hat_w_phi_2"] ** c_1
    K_1_3 = PP["hat_w"] ** c_1
    K_2_1 = MK["hat_g"] ** r_1 * (PP["hat_w_phi_1"] ** c_2)
    K_2_2 = PP["hat_w_phi_2"] ** c_2
    K_2_3 = PP["hat_w"] ** c_2

    for i in range(len_of_ID + 1, max_level + 1):
        tmp_1 = (MK["hat_u_" + str(i)] ** r_1) * (
            PP["hat_w_phi_1"] ** eval("c_3_" + str(i))
        )
        exec(f"L_3_{i}_1 = tmp_1")

        tmp_2 = PP["hat_w_phi_2"] ** eval("c_3_" + str(i))
        exec(f"L_3_{i}_2 = tmp_2")

        tmp_3 = PP["hat_w"] ** eval("c_3_" + str(i))
        exec(f"L_3_{i}_3 = tmp_3")

    r_2 = group.random(ZR)
    c_4 = group.random(ZR)
    c_5 = group.random(ZR)

    for i in range(len_of_ID + 1, max_level + 1):
        exec(f"c_6_{i} = group.random(ZR)")

    tmp = group.init(G2)
    for i in range(1, len_of_ID + 1):
        tmp += MK["hat_u_" + str(i)] ** ID[i - 1]
    tmp_2 = (MK["hat_h"] * tmp) ** r_2
    R_1_1 = tmp_2 * (PP["hat_w_phi_1"] ** c_4)

    R_1_2 = PP["hat_w_phi_2"] ** c_4
    R_1_3 = PP["hat_w"] ** c_4
    R_2_1 = MK["hat_g"] ** r_2 * (PP["hat_w_phi_1"] ** c_5)
    R_2_2 = PP["hat_w_phi_2"] ** c_5
    R_2_3 = PP["hat_w"] ** c_5

    for i in range(len_of_ID + 1, max_level + 1):
        tmp_1 = (MK["hat_u_" + str(i)] ** r_2) * (
            PP["hat_w_phi_1"] ** eval("c_6_" + str(i))
        )
        exec(f"R_3_{i}_1 = tmp_1")

        tmp_2 = PP["hat_w_phi_2"] ** eval("c_6_" + str(i))
        exec(f"R_3_{i}_2 = tmp_2")

        tmp_3 = PP["hat_w"] ** eval("c_6_" + str(i))
        exec(f"R_3_{i}_3 = tmp_3")

    Sk_ID = {
        "ID_string": ID_string,
        "len_of_ID": len_of_ID,
        "K_1_1": K_1_1,
        "K_1_2": K_1_2,
        "K_1_3": K_1_3,
        "K_2_1": K_2_1,
        "K_2_2": K_2_2,
        "K_2_3": K_2_3,
        "R_1_1": R_1_1,
        "R_1_2": R_1_2,
        "R_1_3": R_1_3,
        "R_2_1": R_2_1,
        "R_2_2": R_2_2,
        "R_2_3": R_2_3,
    }

    for i in range(len_of_ID + 1, max_level + 1):

        Sk_ID["L_3_" + str(i) + "_1"] = eval("L_3_" + str(i) + "_1")
        Sk_ID["L_3_" + str(i) + "_2"] = eval("L_3_" + str(i) + "_2")
        Sk_ID["L_3_" + str(i) + "_3"] = eval("L_3_" + str(i) + "_3")
        Sk_ID["R_3_" + str(i) + "_1"] = eval("R_3_" + str(i) + "_1")
        Sk_ID["R_3_" + str(i) + "_2"] = eval("R_3_" + str(i) + "_2")
        Sk_ID["R_3_" + str(i) + "_3"] = eval("R_3_" + str(i) + "_3")

    return Sk_ID


def SkDel(System_para, PP, Sk_ID, Del_ID_string):
    len_of_ID = Sk_ID["len_of_ID"]
    max_level = System_para["max_level"]

    Del_ID = [group.hash(i) for i in Del_ID_string]
    del_len_of_ID = len(Del_ID_string)

    W_1 = PP["hat_w_phi_1"]
    W_2 = PP["hat_w_phi_2"]
    W_3 = PP["hat_w"]

    gamma_1 = group.random(ZR)
    delta_1 = group.random(ZR)
    delta_2 = group.random(ZR)

    for i in range(len_of_ID + 2, max_level + 1):
        exec(f"delta_3_{i} = group.random(ZR)")

    K_1_1 = (
        Sk_ID["K_1_1"]
        * Sk_ID["L_3_" + str(del_len_of_ID) + "_1"] ** Del_ID[del_len_of_ID - 1]
        * (
            Sk_ID["R_1_1"]
            * Sk_ID["R_3_" + str(del_len_of_ID) + "_1"] ** Del_ID[del_len_of_ID - 1]
        )
        ** gamma_1
        * W_1**delta_1
    )

    K_1_2 = (
        Sk_ID["K_1_2"]
        * Sk_ID["L_3_" + str(del_len_of_ID) + "_2"] ** Del_ID[del_len_of_ID - 1]
        * (
            Sk_ID["R_1_2"]
            * Sk_ID["R_3_" + str(del_len_of_ID) + "_2"] ** Del_ID[del_len_of_ID - 1]
        )
        ** gamma_1
        * W_2**delta_1
    )

    K_1_3 = (
        Sk_ID["K_1_3"]
        * Sk_ID["L_3_" + str(del_len_of_ID) + "_3"] ** Del_ID[del_len_of_ID - 1]
        * (
            Sk_ID["R_1_3"]
            * Sk_ID["R_3_" + str(del_len_of_ID) + "_3"] ** Del_ID[del_len_of_ID - 1]
        )
        ** gamma_1
        * W_3**delta_1
    )

    K_2_1 = Sk_ID["K_2_1"] * Sk_ID["R_2_1"] ** gamma_1 * W_1**delta_2
    K_2_2 = Sk_ID["K_2_2"] * Sk_ID["R_2_2"] ** gamma_1 * W_2**delta_2
    K_2_3 = Sk_ID["K_2_3"] * Sk_ID["R_2_3"] ** gamma_1 * W_3**delta_2

    for i in range(len_of_ID + 2, max_level + 1):
        tmp_1 = (
            Sk_ID["L_3_" + str(i) + "_1"]
            * Sk_ID["R_3_" + str(i) + "_1"] ** gamma_1
            * W_1 ** eval("delta_3_" + str(i))
        )
        exec(f"L_3_{i}_1 = tmp_1")

        tmp_2 = (
            Sk_ID["L_3_" + str(i) + "_2"]
            * Sk_ID["R_3_" + str(i) + "_2"] ** gamma_1
            * W_2 ** eval("delta_3_" + str(i))
        )
        exec(f"L_3_{i}_2 = tmp_2")

        tmp_3 = (
            Sk_ID["L_3_" + str(i) + "_3"]
            * Sk_ID["R_3_" + str(i) + "_3"] ** gamma_1
            * W_3 ** eval("delta_3_" + str(i))
        )
        exec(f"L_3_{i}_3 = tmp_3")

    gamma_2 = group.random(ZR)
    delta_4 = group.random(ZR)
    delta_5 = group.random(ZR)

    for i in range(len_of_ID + 2, max_level + 1):
        exec(f"delta_6_{i} = group.random(ZR)")

    R_1_1 = (
        Sk_ID["R_1_1"]
        * Sk_ID["R_3_" + str(len_of_ID + 1) + "_1"] ** Del_ID[del_len_of_ID - 1]
    ) ** gamma_2 * W_1**delta_4

    R_1_2 = (
        Sk_ID["R_1_2"]
        * Sk_ID["R_3_" + str(len_of_ID + 1) + "_2"] ** Del_ID[del_len_of_ID - 1]
    ) ** gamma_2 * W_2**delta_4

    R_1_3 = (
        Sk_ID["R_1_3"]
        * Sk_ID["R_3_" + str(len_of_ID + 1) + "_3"] ** Del_ID[del_len_of_ID - 1]
    ) ** gamma_2 * W_3**delta_4

    R_2_1 = Sk_ID["R_2_1"] ** gamma_2 * W_1**delta_5
    R_2_2 = Sk_ID["R_2_2"] ** gamma_2 * W_2**delta_5
    R_2_3 = Sk_ID["R_2_3"] ** gamma_2 * W_3**delta_5

    for i in range(len_of_ID + 2, max_level + 1):
        tmp_1 = Sk_ID["R_3_" + str(i) + "_1"] ** gamma_2 * W_1 ** eval(
            "delta_6_" + str(i)
        )
        exec(f"R_3_{i}_1 = tmp_1")

        tmp_2 = Sk_ID["R_3_" + str(i) + "_2"] ** gamma_2 * W_2 ** eval(
            "delta_6_" + str(i)
        )
        exec(f"R_3_{i}_2 = tmp_2")

        tmp_3 = Sk_ID["R_3_" + str(i) + "_3"] ** gamma_2 * W_3 ** eval(
            "delta_6_" + str(i)
        )
        exec(f"R_3_{i}_3 = tmp_3")

    Sk_Del_ID = {
        "ID_string": Del_ID_string,
        "len_of_ID": del_len_of_ID,
        "K_1_1": K_1_1,
        "K_1_2": K_1_2,
        "K_1_3": K_1_3,
        "K_2_1": K_2_1,
        "K_2_2": K_2_2,
        "K_2_3": K_2_3,
        "R_1_1": R_1_1,
        "R_1_2": R_1_2,
        "R_1_3": R_1_3,
        "R_2_1": R_2_1,
        "R_2_2": R_2_2,
        "R_2_3": R_2_3,
    }

    for i in range(len_of_ID + 2, max_level + 1):
        Sk_Del_ID["L_3_" + str(i) + "_1"] = eval("L_3_" + str(i) + "_1")
        Sk_Del_ID["L_3_" + str(i) + "_2"] = eval("L_3_" + str(i) + "_2")
        Sk_Del_ID["L_3_" + str(i) + "_3"] = eval("L_3_" + str(i) + "_3")
        Sk_Del_ID["R_3_" + str(i) + "_1"] = eval("R_3_" + str(i) + "_1")
        Sk_Del_ID["R_3_" + str(i) + "_2"] = eval("R_3_" + str(i) + "_2")
        Sk_Del_ID["R_3_" + str(i) + "_3"] = eval("R_3_" + str(i) + "_3")

    return Sk_Del_ID


def Enc(System_para, PP, receiver_ID_string, plaintext):
    max_level = System_para["max_level"]

    ID = [group.hash(i) for i in receiver_ID_string]
    len_of_ID = len(receiver_ID_string)

    key = group.random(GT)

    t = group.random(ZR)
    C = PP["Sigma"] ** t * key
    C_1_1 = PP["g"] ** t
    C_1_2 = PP["g_v"] ** t
    C_1_3 = PP["g_minus_tau"] ** t

    tmp_1 = group.init(G1)
    for i in range(1, len_of_ID + 1):
        tmp_1 += PP["u_" + str(i)] ** ID[i - 1]

    C_2_1 = (PP["h"] * tmp_1) ** t

    tmp_2 = group.init(G1)
    for i in range(1, len_of_ID + 1):
        tmp_2 += PP["u_v_" + str(i)] ** ID[i - 1]

    C_2_2 = (PP["h_v"] * tmp_2) ** t

    tmp_3 = group.init(G1)
    for i in range(1, len_of_ID + 1):
        tmp_3 += PP["u_minus_tau_" + str(i)] ** ID[i - 1]

    C_2_3 = (PP["h_minus_tau"] * tmp_3) ** t

    enc_cipher = AuthenticatedCryptoAbstraction(extract_key(key))
    Enc_message = enc_cipher.encrypt(plaintext)

    Enc_key = {
        "C": C,
        "C_1_1": C_1_1,
        "C_1_2": C_1_2,
        "C_1_3": C_1_3,
        "C_2_1": C_2_1,
        "C_2_2": C_2_2,
        "C_2_3": C_2_3,
    }

    return Enc_key, Enc_message


def Dec(System_para, PP, receiver_Sk, Enc_key, Enc_message):

    dec_key = (
        Enc_key["C"]
        * (pair(Enc_key["C_1_1"], receiver_Sk["K_1_1"]) ** -1)
        * (pair(Enc_key["C_1_2"], receiver_Sk["K_1_2"]) ** -1)
        * (pair(Enc_key["C_1_3"], receiver_Sk["K_1_3"]) ** -1)
        * pair(Enc_key["C_2_1"], receiver_Sk["K_2_1"])
        * pair(Enc_key["C_2_2"], receiver_Sk["K_2_2"])
        * pair(Enc_key["C_2_3"], receiver_Sk["K_2_3"])
    )

    dec_cipher = AuthenticatedCryptoAbstraction(extract_key(dec_key))
    result = dec_cipher.decrypt(Enc_message)
    return result


def Serialize_CT(System_para, Enc_key, Enc_message):

    tmp = b""
    for k, v in Enc_key.items():
        tmp += group.serialize(v)

    result = tmp.decode("utf-8") + str(Enc_message)

    return result


def De_serialize_CT(System_para, serialize_CT):

    C = group.deserialize(serialize_CT[0:162])
    C_1_1 = group.deserialize(serialize_CT[162:192])
    C_1_2 = group.deserialize(serialize_CT[192:222])
    C_1_3 = group.deserialize(serialize_CT[222:252])
    C_2_1 = group.deserialize(serialize_CT[252:282])
    C_2_2 = group.deserialize(serialize_CT[282:312])
    C_2_3 = group.deserialize(serialize_CT[312:342])
    Enc_message = eval(serialize_CT[342:].decode("utf-8"))

    Enc_key = {
        "C": C,
        "C_1_1": C_1_1,
        "C_1_2": C_1_2,
        "C_1_3": C_1_3,
        "C_2_1": C_2_1,
        "C_2_2": C_2_2,
        "C_2_3": C_2_3,
    }

    Vrfy_CT = serialize_CT[0:342].decode("utf-8") + serialize_CT[342:].decode("utf-8")

    return Vrfy_CT, Enc_key, Enc_message


if __name__ == "__main__":
    
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
    Enc_key, Enc_message = Enc(System_para, PP, receiver_ID_string, plaintext)
    end4 = time.time()

    receiver_Sk = Sk_Del_ID

    start5 = time.time()
    result = Dec(System_para, PP, receiver_Sk, Enc_key, Enc_message)
    end5 = time.time()

    print("Setup:%f s" % (end1 - start1))
    print("SkGen:%f s" % (end2 - start2))
    print("SkDel:%f s" % (end3 - start3))
    print("Enc:%f s" % (end4 - start4))
    print("Dec:%f s" % (end5 - start5))
