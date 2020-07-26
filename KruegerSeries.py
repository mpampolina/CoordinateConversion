def getAlphaSeries(n):
    a1 = ((1 / 2) * n - (2 / 3) * n ** 2 + (5 / 16) * n ** 3 + (41 / 180) * n ** 4 - (127 / 288) * n ** 5 + (
            7891 / 37800) * n ** 6 + (72161 / 387072) * n ** 7
          - (18975107 / 50803200) * n ** 8 + (60193001 / 290304000) * n ** 9 + (134592031 / 1026432000) * n ** 10)
    a2 = ((13 / 48) * n ** 2 - (3 / 5) * n ** 3 + (557 / 1440) * n ** 4 + (281 / 630) * n ** 5 - (
            1983433 / 1935360) * n ** 6 + (13769 / 28800) * n ** 7 +
          (148003883 / 174182400) * n ** 8 - (705286231 / 465696000) * n ** 9 + (
                  1703267974087 / 3218890752000) * n ** 10)
    a3 = ((61 / 240) * n ** 3 - (103 / 140) * n ** 4 + (15061 / 26880) * n ** 5 + (167603 / 181440) * n ** 6 - (
            67102379 / 29030400) * n ** 7 +
          (79682431 / 79833600) * n ** 8 + (6304945039 / 2128896000) * n ** 9 - (
                  6601904925257 / 1307674368000) * n ** 10)
    a4 = ((49561 / 161280) * n ** 4 - (179 / 168) * n ** 5 + (6601661 / 7257600) * n ** 6 + (97445 / 49896) * n ** 7 -
          (40176129013 / 7664025600) * n ** 8 + (138471097 / 66528000) * n ** 9 + (
                  48087451385201 / 5230697472000) * n ** 10)
    a5 = ((34729 / 80640) * n ** 5 - (3418889 / 1995840) * n ** 6 + (14644087 / 9123840) * n ** 7 + (
            2605413599 / 622702080) * n ** 8 -
          (31015475399 / 2583060480) * n ** 9 + (5820486440369 / 1307674368000) * n ** 10)
    a6 = ((212378941 / 319334400) * n ** 6 - (30705481 / 10378368) * n ** 7 + (175214326799 / 58118860800) * n ** 8 +
          (870492877 / 96096000) * n ** 9 - (1328004581729000 / 47823519744000) * n ** 10)
    a7 = ((1522256789 / 1383782400) * n ** 7 - (16759934899 / 3113510400) * n ** 8 + (
            1315149374443 / 221405184000) * n ** 9 +
          (71809987837451 / 3629463552000) * n ** 10)

    return a1, a2, a3, a4, a5, a6, a7


def getBetaSeries(n):
    b1 = ((1 / 2) * n - (2 / 3) * n ** 2 + (37 / 96) * n ** 3 - (1 / 360) * n ** 4 - (81 / 512) * n ** 5 + (
                96199 / 604800) * n ** 6 - (5406467 / 38707200) * n ** 7 +
          (7944359 / 67737600) * n ** 8 - (7378753979 / 97542144000) * n ** 9 + (25123531261 / 804722688000) * n ** 10)
    b2 = ((1 / 48) * n ** 2 + (1 / 15) * n ** 3 - (437 / 1440) * n ** 4 + (46 / 105) * n ** 5 - (
                1118711 / 3870720) * n ** 6 + (51841 / 1209600) * n ** 7 +
          (24749483 / 348364800) * n ** 8 - (115295683 / 1397088000) * n ** 9 + (
                      5487737251099 / 51502252032000) * n ** 10)
    b3 = ((17 / 480) * n ** 3 - (37 / 840) * n ** 4 - (209 / 4480) * n ** 5 + (5569 / 90720) * n ** 6 + (
                9261899 / 58060800) * n ** 7 -
          (6457463 / 17740800) * n ** 8 + (2473691167 / 9289728000) * n ** 9 - (
                      852549456029 / 20922789888000) * n ** 10)
    b4 = ((4397 / 161280) * n ** 4 - (11 / 504) * n ** 5 - (830251 / 7257600) * n ** 6 + (466511 / 2494800) * n ** 7 + (
                324154477 / 7664025600) * n ** 8
          - (937932223 / 3891888000) * n ** 9 - (89112264211 / 5230697472000) * n ** 10)
    b5 = ((4583 / 161280) * n ** 5 - (108847 / 3991680) * n ** 6 - (8005831 / 63866880) * n ** 7 + (
                22894433 / 124540416) * n ** 8 +
          (112731569449 / 557941063680) * n ** 9 - (5391039814733 / 10461394944000) * n ** 10)
    b6 = ((20648693 / 638668800) * n ** 6 - (16363163 / 518918400) * n ** 7 - (2204645983 / 12915302400) * n ** 8 +
          (4543317553 / 18162144000) * n ** 9 + (54894890298749 / 167382319104000) * n ** 10)
    b7 = ((219941297 / 5535129600) * n ** 7 - (497323811 / 12454041600) * n ** 8 - (
                79431132943 / 332107776000) * n ** 9 +
          (4346429528407 / 12703122432000) * n ** 10)

    return b1, b2, b3, b4, b5, b6, b7
