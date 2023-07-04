from charm.toolbox.ecgroup import ECGroup, ZR, G
from charm.toolbox.eccurve import secp160r1
import math

group = ECGroup(secp160r1)


def Setup():
    g_1 = group.random(G)
    x = group.random(ZR)
    x_p = group.random(ZR)
    g_2 = g_1**x
    g_3 = g_1**x_p

    r = group.random(ZR)
    r_p = group.random(ZR)

    z_0 = group.hash(g_1 * g_2**r)
    z_1 = group.hash(g_1 * g_3**r_p)

    Ovk = {"g_1": g_1, "g_2": g_2, "g_3": g_3, "z_0": z_0}
    Osk = {"y": x**-1, "y_p": x_p**-1, "r": r, "r_p": r_p, "z_1": z_1}
    System_para = {"group": group}

    return Osk, Ovk


def Sign(Osk, plaintext):
    hash_plaintext = group.hash(plaintext)

    sigma_0 = Osk["y_p"] * (1 - hash_plaintext) + Osk["r_p"]
    sigma_1 = Osk["y"] * (1 - Osk["z_1"]) + Osk["r"]

    sigma = {"sigma_0": sigma_0, "sigma_1": sigma_1}
    return sigma


def Vrfy(Ovk, sigma, plaintext):
    hash_plaintext = group.hash(plaintext)

    tmp = (
        Ovk["g_1"]
        ** group.hash(Ovk["g_1"] ** hash_plaintext * Ovk["g_3"] ** sigma["sigma_0"])
        * Ovk["g_2"] ** sigma["sigma_1"]
    )
    result = group.hash(tmp) == Ovk["z_0"]
    return result


def Serialize_Ovk(Ovk):

    tmp = b""

    for k, v in Ovk.items():
        tmp += group.serialize(v)
    result = tmp
    return result


if __name__ == "__main__":

    Osk, Ovk = Setup()

    plaintext = "Hello"
    sigma = Sign(Osk, plaintext)
    result = Vrfy(Ovk, sigma, plaintext)
    print(result)
