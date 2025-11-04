# 📝 Zincirleme Etki (Chain Reaction) Oyunu için Minimax AI Raporu

## 1. Giriş

Bu rapor, Pygame kütüphanesi kullanılarak geliştirilen ve Alpha-Beta Budamalı Minimax algoritması ile güçlendirilmiş bir yapay zeka (AI) ajanı içeren Zincirleme Etki (Chain Reaction) tahta oyununun teknik uygulamasını detaylandırmaktadır. Projenin temel amacı, klasik bir strateji oyunu ortamında en iyi hamleyi bulabilen verimli bir AI ajanı oluşturmaktır.

## 2. Oyun Mekanikleri ve Uygulama (OyunTahtasi Sınıfı)

### 2.1. Tahta Temsili ve Oyuncu Kimlikleri

Oyun tahtası, 8x8 boyutlarında bir matris (`self.tahta`) ile temsil edilir. Karelerin değerleri, hangi oyuncuya ait olduğunu gösteren kimlik (ID) numaraları ile temsil edilir:

* **Boş Kare:** `0`
* **AI (Kırmızı):** `1` (`self.ai_id`)
* **İnsan Oyuncu (Mavi):** `2` (`self.insan_id`)

Oyuncu sırası, `self.oyuncu_sira = 3 - oyuncu_id` basit aritmetik formülü kullanılarak tutarlı bir şekilde değiştirilir.

### 2.2. Zincirleme Etki Mekaniği (`zincirleme_etkiyi_kontrol_et`)

Oyunun temel mekaniği, bir oyuncunun hamlesi sonrası yatay, dikey veya çapraz yönde 4 veya daha fazla puldan oluşan zincirleri tespit etmektir.

* **Puanlama:** Oluşturulan zincirdeki pul sayısı kadar oyuncunun skoruna puan eklenir.
* **Tahtadan Kaldırma:** Puanlanan zincirdeki tüm pullar, puanlama tamamlandıktan sonra tahtadan kaldırılır (`0` olarak ayarlanır), bu da stratejik boşluklar yaratarak oyuna dinamizm katar.

### 2.3. Oyun Sonu Koşulları

Oyun iki ana koşuldan biri gerçekleştiğinde sona erer:

1.  **Skor Limiti:** Bir oyuncunun skoru belirlenen limite (`limit_skor = 30`) ulaştığında.
2.  **Tahta Doluluğu:** Tahtada geçerli hamle kalmadığında (tüm kareler dolduğunda). Bu durumda en yüksek skora sahip oyuncu kazanır.

## 3. Yapay Zeka Ajanı (MinimaxAgent Sınıfı)

AI ajanı, tam bilgiye sahip, sıfır toplamlı bu oyun için optimal stratejiyi bulmaya çalışan **Minimax algoritmasını** kullanır.

### 3.1. Minimax Algoritması

Minimax, her bir oyun durumu için sayısal bir değer (skor) atayarak, AI'ın kazancını maksimize etmeye ve rakibin (İnsan) kazancını minimize etmeye odaklanır.

* **Maksimize Eden Oyuncu (Maximizing Player):** AI (`self.ai_id = 1`). Amacı en yüksek skoru bulmaktır.
* **Minimize Eden Oyuncu (Minimizing Player):** İnsan (`self.insan_id = 2`). Amacı AI için en düşük skoru bulmaktır.
* **Derinlik (`derinlik`):** Ajanın ne kadar ileriye bakacağını belirler. Bu projede **varsayılan derinlik 2** olarak ayarlanmıştır.

### 3.2. Alpha-Beta Budaması (Alpha-Beta Pruning)

Minimax arama ağacının verimliliğini artırmak için **Alpha-Beta Budaması** tekniği uygulanmıştır.

* **Alpha Değeri:** Maksimize eden oyuncunun (AI) o ana kadar bulduğu en iyi garantili skor.
* **Beta Değeri:** Minimize eden oyuncunun (İnsan) o ana kadar bulduğu en kötü (AI için) garantili skor.
* **Budama Koşulu:** Eğer **Beta $\le$ Alpha** ise, ağacın mevcut dalı daha fazla incelenmeden kesilir (budanır), çünkü bu dalın daha kötü bir sonuç vereceği garantilenmiştir. Bu, arama süresini önemli ölçüde kısaltır.

### 3.3. Değerlendirme Fonksiyonu (Heuristik)

Oyun sonu durumlarında kesin skorlar verilirken ($10^6$ ve $-10^6$), ara durumlarda tahtayı sayısal olarak değerlendiren bir sezgisel (heuristik) fonksiyon (`degerlendirme_fonksiyonu`) kullanılır.

$$
\text{Skor} = (\text{AI Skor} - \text{İnsan Skor}) \times 100 + \text{Merkez Değeri}
$$

**Heuristik Bileşenleri:**

1.  **Skor Farkı ($\times 100$):** Mevcut skor farkı, tahtanın mevcut durumunun ana belirleyicisidir ve ağırlıklandırılarak (100 ile çarpılarak) önceliklendirilir.
2.  **Merkez Kontrolü (Merkez Değeri):** Tahtanın merkezi kareleri $[(3, 3), (3, 4), (4, 3), (4, 4)]$ stratejik öneme sahiptir. Bu karelere sahip olmak AI için $+5$, İnsan için $-5$ puan olarak eklenir.

## 4. Sonuç ve Geliştirme Önerileri

Bu projede, Minimax algoritması ve Alpha-Beta Budaması kullanılarak Chain Reaction oyun kurallarına uyan güçlü bir AI ajanı başarıyla oluşturulmuştur. AI, özellikle merkez kontrolünü ve skor farkını maksimize etmeye odaklanan sezgisel fonksiyon sayesinde stratejik hamleler yapabilmektedir.

### Geliştirme Önerileri:

* **Derinlik Artışı:** Donanım elverdiğince arama derinliğini artırmak, AI'ın öngörüsünü ve performansını yükseltir.
* **Gelişmiş Heuristik:** Kenar pullarına sahip olmaya ek puan vermek veya zincir potansiyelini (3'lü veya 2'li grupların sayısını) hesaba katmak gibi daha karmaşık sezgisel faktörler eklenebilir.
* **İteratif Derinleştirme:** Daha uzun süreli düşünme sürelerinde dahi stabil tepki süreleri sağlamak için Minimax'a İteratif Derinleştirme (Iterative Deepening) tekniği uygulanabilir.