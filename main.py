import pygame
import sys
from minimax_agent import MinimaxAgent

tahta_boyut = 8
kare_boyut = 75
ekran_genislik = tahta_boyut * kare_boyut
ekran_yukseklik = ekran_genislik + 50
limit_skor = 30

beyaz = (255, 255, 255)
siyah = (0, 0, 0)
kirmizi = (255, 0, 0)
mavi = (0, 0, 255)
arka_plan = (230, 230, 230)

pygame.init()
ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))
pygame.display.set_caption("Zincirleme Etki (Chain Reaction) - AI Projesi")
font = pygame.font.Font(None, 30)

class OyunTahtasi:
    def __init__(self):
        self.tahta = [[0 for _ in range(tahta_boyut)] for _ in range(tahta_boyut)]
        self.skorlar = {1: 0, 2: 0}
        self.oyuncu_sira = 2
        self.oyun_sonu = False
        self.kazanan = None

    def gecerli_hamleleri_al(self):
        hamleler = []
        for r in range(tahta_boyut):
            for c in range(tahta_boyut):
                if self.tahta[r][c] == 0:
                    hamleler.append((r, c))
        return hamleler

    def hamle_yap(self, satir, sutun, oyuncu_id):
        if self.tahta[satir][sutun] != 0 or self.oyun_sonu:
            return False

        self.tahta[satir][sutun] = oyuncu_id

        puan, kaldirilacak = self.zincirleme_etkiyi_kontrol_et(satir, sutun, oyuncu_id)
        self.skorlar[oyuncu_id] += puan

        for r, c in kaldirilacak:
            self.tahta[r][c] = 0

        self.oyuncu_sira = 3 - oyuncu_id

        if self.skorlar[oyuncu_id] >= limit_skor:
            self.oyun_sonu = True
            self.kazanan = oyuncu_id
        elif not self.gecerli_hamleleri_al():
            self.oyun_sonu = True
            self.kazanan = 1 if self.skorlar[1] > self.skorlar[2] else (2 if self.skorlar[2] > self.skorlar[1] else 0)

        return True

    def zincirleme_etkiyi_kontrol_et(self, r, c, oyuncu_id):
        puan = 0
        kaldirilacak_pullar = set()
        yonler = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in yonler:
            zincir = set()
            sayac = 0

            for i in range(1, 4):
                nr, nc = r + dr * i * (-1), c + dc * i * (-1)
                if 0 <= nr < tahta_boyut and 0 <= nc < tahta_boyut and self.tahta[nr][nc] == oyuncu_id:
                    zincir.add((nr, nc))
                    sayac += 1
                else:
                    break

            zincir.add((r, c))
            sayac += 1

            for i in range(1, 4):
                nr, nc = r + dr * i * (1), c + dc * i * (1)
                if 0 <= nr < tahta_boyut and 0 <= nc < tahta_boyut and self.tahta[nr][nc] == oyuncu_id:
                    zincir.add((nr, nc))
                    sayac += 1
                else:
                    break

            if sayac >= 4:
                puan += sayac
                kaldirilacak_pullar.update(zincir)

        return puan, kaldirilacak_pullar

    def tahtayi_kopyala(self):
        yeni_tahta = OyunTahtasi()
        yeni_tahta.tahta = [row[:] for row in self.tahta]
        yeni_tahta.skorlar = self.skorlar.copy()
        yeni_tahta.oyuncu_sira = self.oyuncu_sira
        yeni_tahta.oyun_sonu = self.oyun_sonu
        yeni_tahta.kazanan = self.kazanan
        return yeni_tahta

def tahtayi_ciz(tahta):
    ekran.fill(arka_plan)
    for r in range(tahta_boyut):
        for c in range(tahta_boyut):
            rect = pygame.Rect(c * kare_boyut, r * kare_boyut, kare_boyut, kare_boyut)
            pygame.draw.rect(ekran, siyah, rect, 1)

            pul_renk = None
            if tahta.tahta[r][c] == 1:
                pul_renk = kirmizi
            elif tahta.tahta[r][c] == 2:
                pul_renk = mavi

            if pul_renk:
                merkez_x = c * kare_boyut + kare_boyut // 2
                merkez_y = r * kare_boyut + kare_boyut // 2
                pygame.draw.circle(ekran, pul_renk, (merkez_x, merkez_y), kare_boyut // 2 - 5)

    skor_text_1 = font.render(f"AI (Kırmızı): {tahta.skorlar[1]}", True, kirmizi)
    skor_text_2 = font.render(f"Oyuncu (Mavi): {tahta.skorlar[2]}", True, mavi)

    ekran.blit(skor_text_1, (10, ekran_genislik + 10))
    ekran.blit(skor_text_2, (ekran_genislik - skor_text_2.get_width() - 10, ekran_genislik + 10))

    if tahta.oyun_sonu:
        mesaj = ""
        if tahta.kazanan == 1:
            mesaj = "AI (Kırmızı) Kazandı!"
            renk = kirmizi
        elif tahta.kazanan == 2:
            mesaj = "Oyuncu (Mavi) Kazandı!"
            renk = mavi
        else:
            mesaj = "Berabere!"
            renk = siyah

        sonuc_text = font.render(mesaj, True, renk)
        mesaj_rect = sonuc_text.get_rect(center=(ekran_genislik // 2, ekran_genislik // 2))

        arka_rect = mesaj_rect.inflate(20, 10)
        pygame.draw.rect(ekran, beyaz, arka_rect)
        pygame.draw.rect(ekran, siyah, arka_rect, 2)
        ekran.blit(sonuc_text, mesaj_rect)

    pygame.display.flip()

def main():
    tahta = OyunTahtasi()
    ai_agent = MinimaxAgent(derinlik=2)

    ai_hamle_zamani = 0
    ai_gecikme_ms = 999

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if tahta.oyuncu_sira == 2 and not tahta.oyun_sonu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    sutun = pos[0] // kare_boyut
                    satir = pos[1] // kare_boyut
                    if 0 <= satir < tahta_boyut and 0 <= sutun < tahta_boyut and tahta.tahta[satir][sutun] == 0:
                        tahta.hamle_yap(satir, sutun, 2)
                        if tahta.oyuncu_sira == 1:
                            ai_hamle_zamani = pygame.time.get_ticks() + ai_gecikme_ms

        if tahta.oyuncu_sira == 1 and not tahta.oyun_sonu:
            if pygame.time.get_ticks() > ai_hamle_zamani:
                gecerli_hamleler = tahta.gecerli_hamleleri_al()
                if gecerli_hamleler:
                    r, c = ai_agent.minimax_ara(tahta)
                    tahta.hamle_yap(r, c, 1)

        tahtayi_ciz(tahta)

if __name__ == "__main__":
    main()