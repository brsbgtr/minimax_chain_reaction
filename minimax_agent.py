class MinimaxAgent:

    def __init__(self, derinlik=2):
        self.max_derinlik = derinlik
        self.ai_id = 1
        self.insan_id = 2

    def minimax_ara(self, oyun_tahtası): #Şu anki tahtada AI en iyi nereye oynasın?
        en_iyi_skor = -float('inf') #Başlangıçta en kötü olasılık varsayılır
        en_iyi_hamle = None

        gecerli_hamleler = oyun_tahtası.gecerli_hamleleri_al() #Boş kareleri döndürüyor

        for hamle in gecerli_hamleler:
            r, c = hamle #satır,sütun
            deneme_tahtası = oyun_tahtası.tahtayi_kopyala() #asıl tahtayı bozmamak için kopya
            deneme_tahtası.hamle_yap(r, c, self.ai_id)

            hamle_skoru = self.minimax(deneme_tahtası, 0, False, -float('inf'), float('inf'))

            if hamle_skoru > en_iyi_skor:
                en_iyi_skor = hamle_skoru
                en_iyi_hamle = hamle

        return en_iyi_hamle

    def minimax(self, oyun_tahtası, derinlik, maximizing_player, alpha, beta):
        if derinlik == self.max_derinlik or oyun_tahtası.oyun_sonu:
            return self.degerlendirme_fonksiyonu(oyun_tahtası)

        if maximizing_player: #AI maximize etmeye çalışır
            en_iyi_skor = -float('inf')
            for hamle in oyun_tahtası.gecerli_hamleleri_al():
                deneme_tahtası = oyun_tahtası.tahtayi_kopyala()
                deneme_tahtası.hamle_yap(hamle[0], hamle[1], self.ai_id)

                skor = self.minimax(deneme_tahtası, derinlik + 1, False, alpha, beta) #İnsan şimdi ne yapar? Simüle ediyoruz
                en_iyi_skor = max(en_iyi_skor, skor)

                alpha = max(alpha, skor) #Alfa-beta budaması -> Gereksiz dalları kesmek için
                if beta <= alpha:
                    break
            return en_iyi_skor

        else:
            en_kotu_skor = float('inf')
            for hamle in oyun_tahtası.gecerli_hamleleri_al():
                deneme_tahtası = oyun_tahtası.tahtayi_kopyala()
                deneme_tahtası.hamle_yap(hamle[0], hamle[1], self.insan_id)

                skor = self.minimax(deneme_tahtası, derinlik + 1, True, alpha, beta) #AI ne düşünür,simüle ediyoruz
                en_kotu_skor = min(en_kotu_skor, skor)

                beta = min(beta, skor) #Alfa-beta budaması -> Gereksiz dalları kesmek için
                if beta <= alpha:
                    break
            return en_kotu_skor

    def degerlendirme_fonksiyonu(self, oyun_tahtası):
        if oyun_tahtası.oyun_sonu:
            if oyun_tahtası.kazanan == self.ai_id:
                return 10**6
            elif oyun_tahtası.kazanan == self.insan_id:
                return -10**6
            else:
                return 0

        skor_farki = oyun_tahtası.skorlar[self.ai_id] - oyun_tahtası.skorlar[self.insan_id]

        merkez_degeri = 0
        merkez_kareler = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for r, c in merkez_kareler:
            if oyun_tahtası.tahta[r][c] == self.ai_id:
                merkez_degeri += 5
            elif oyun_tahtası.tahta[r][c] == self.insan_id:
                merkez_degeri -= 5

        return skor_farki * 100 + merkez_degeri