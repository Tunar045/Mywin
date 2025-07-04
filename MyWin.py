from customtkinter import *
import pyautogui
from PIL import Image, ImageTk
from tkinter import Canvas, filedialog
import datetime
import json
import tkinter as tk
import os

# --- Varliklarin (assets) yolu, goreceli yol kullanmak en iyisidir ---
# Bu, programin herhangi bir dizinden calismasini saglar.
# Bu betigin oldugu yerde 'assets' adinda bir klasor oldugundan emin olun.
# 'd:/Uygulama/MyWin/' yolunuza göre ayarlayın
BASE_DIR = "d:/Uygulama/MyWin/"
VARLIK_YOLU = os.path.join(BASE_DIR, "assets") + os.sep
ARKA_PLAN_AYARLARI_YOLU = os.path.join(BASE_DIR, "arka_plan_ayarlari.json")
METIN_DOSYASI_YOLU = os.path.join(BASE_DIR, "Metin.json")


# --- Temel Ayarlar ---
set_appearance_mode("light")
ekran_genisligi, ekran_yuksekligi = pyautogui.size()

pencere = CTk()
pencere.geometry(f"{ekran_genisligi}x{ekran_yuksekligi}")
pencere.attributes("-fullscreen", True)
pencere.resizable(False, False)
pencere.lift()
pencere.focus_force()

# --- Arka Plan Ayarları ve Global Değişkenler ---
arka_plan_etiketi = CTkLabel(pencere, text="")
arka_plan_etiketi.place(x=0, y=0, relwidth=1, relheight=1)
arka_plan_resmi_referansi = [None] # Garbage collection'ı önlemek için

# Zaman etiketi global olarak tanımlanmalı
zaman_etiketi = None # Başlangıçta None olarak ayarla

# Arka plan resmi varlığını takip etmek için yeni bir global bayrak
arka_plan_resmi_mevcut = False

# Görev çubuğundaki zaman butonu (ileride zamani_guncelle'de kullanılacak)
# Fonksiyon tanımından önce oluşturulması gerekiyor
gorev_cubugu_cercevesi = CTkFrame(pencere, width=400, height=50,corner_radius=1, fg_color="#000000")
gorev_cubugu_cercevesi.pack(side="bottom", fill="x")
gorev_cubugu_cercevesi.pack_propagate(False) # Cercevenin icerigine gore kuculmesini engeller

# Zaman butonu tanımı
zaman_butonu = CTkButton(gorev_cubugu_cercevesi, text="", command=lambda: None, width=50, height=50, corner_radius=5, fg_color="#000000", hover_color="#111111")
zaman_butonu.pack(side="right", padx=5, pady=5)
zaman_butonu.bind("<Enter>", lambda olay, b=zaman_butonu: uzerine_gelince(b))
zaman_butonu.bind("<Leave>", lambda olay, b=zaman_butonu: uzerinden_ayrilinca(b))

# --- Yardimci Fonksiyon: Zaman Etiketini Oluştur/Güncelle ---
def _zaman_etiketini_olustur_ve_guncelle():
    global zaman_etiketi
    if zaman_etiketi and zaman_etiketi.winfo_exists(): # Zaten varsa yeniden oluşturma
        zaman_etiketi.place(relx=0.5, rely=0.4, anchor="center") # Tekrar görünür yap
        # zamani_guncelle() # Metni güncelle, bu zaten ana döngüde yapılıyor
        return

    # Zaman etiketini oluştur
    zaman_etiketi = CTkLabel(pencere, text="", font=("Arial", 80, "bold"), text_color="#000000", fg_color="transparent")
    zaman_etiketi.place(relx=0.5, rely=0.4, anchor="center")

def arka_plan_resmi_ayarla(resim_yolu):
    global arka_plan_resmi_referansi, zaman_etiketi, arka_plan_resmi_mevcut
    print(f"arka_plan_resmi_ayarla çağrıldı. Resim yolu: {resim_yolu}") # DEBUG

    if resim_yolu:
        try:
            img = Image.open(resim_yolu)
            img = img.resize((ekran_genisligi, ekran_yuksekligi), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            arka_plan_etiketi.configure(image=photo)
            arka_plan_etiketi.image = photo
            arka_plan_resmi_referansi[0] = photo
            
            arka_plan_resmi_mevcut = True
            print("Arka plan resmi başarıyla yüklendi. arka_plan_resmi_mevcut =", arka_plan_resmi_mevcut) # DEBUG

            if zaman_etiketi and zaman_etiketi.winfo_exists():
                zaman_etiketi.place_forget()
                print("Büyük zaman etiketi gizlendi.") # DEBUG

            with open(ARKA_PLAN_AYARLARI_YOLU, "w") as f:
                json.dump({"resim_yolu": resim_yolu}, f)

        except Exception as e:
            print(f"HATA: Arka plan resmi yüklenirken hata oluştu: {e}") # DEBUG
            arka_plan_resmi_mevcut = False
            if not zaman_etiketi or not zaman_etiketi.winfo_exists():
                _zaman_etiketini_olustur_ve_guncelle()
            print("Hata durumunda arka_plan_resmi_mevcut =", arka_plan_resmi_mevcut) # DEBUG

    else:
        print("Arka plan resmi sıfırlanıyor.") # DEBUG
        arka_plan_etiketi.configure(image=None)
        arka_plan_etiketi.image = None
        arka_plan_resmi_referansi[0] = None
        
        arka_plan_resmi_mevcut = False
        print("Arka plan resmi sıfırlandı. arka_plan_resmi_mevcut =", arka_plan_resmi_mevcut) # DEBUG

        if os.path.exists(ARKA_PLAN_AYARLARI_YOLU):
            os.remove(ARKA_PLAN_AYARLARI_YOLU)
        
        if not zaman_etiketi or not zaman_etiketi.winfo_exists():
            _zaman_etiketini_olustur_ve_guncelle()
    
    zamani_guncelle()


# ... (Diğer kodlar) ...

def zamani_guncelle():
    global zaman_etiketi, arka_plan_resmi_mevcut
    if zaman_etiketi and zaman_etiketi.winfo_exists():
        if not arka_plan_resmi_mevcut:
            zaman_etiketi.configure(text=datetime.datetime.now().strftime("%H:%M"))
            zaman_etiketi.place(relx=0.5, rely=0.4, anchor="center")
        else:
            zaman_etiketi.place_forget()

    if arka_plan_resmi_mevcut:
        zaman_butonu.configure(text=datetime.datetime.now().strftime("%H:%M\n%d.%m.%Y"))
    else:
        saat_dakika_gun_ay_yil = datetime.datetime.now().strftime("%H:%M\n%d.%m.%Y")
        zaman_butonu.configure(text=saat_dakika_gun_ay_yil)
    
    pencere.after(1000, zamani_guncelle)

# ... (Kodun geri kalanı) ...


# Uygulama başlangıcında kaydedilmiş arka planı yükle
try:
    with open(ARKA_PLAN_AYARLARI_YOLU, "r") as f:
        ayarlar = json.load(f)
        if "resim_yolu" in ayarlar:
            arka_plan_resmi_ayarla(ayarlar["resim_yolu"])
            # arka_plan_resmi_mevcut zaten arka_plan_resmi_ayarla içinde ayarlanıyor
except (FileNotFoundError, json.JSONDecodeError):
    arka_plan_resmi_mevcut = False # Dosya yoksa veya bozuksa resim yok demektir

# Eğer uygulama başlangıcında arka plan yüklenmediyse, zaman etiketini oluştur
if not arka_plan_resmi_mevcut and not zaman_etiketi: # zaman_etiketi'nin zaten oluşturulmadığından emin olun
    _zaman_etiketini_olustur_ve_guncelle()


# Acik uygulama pencerelerini takip etmek icin genel liste
acik_pencereler = []
# Baslat Menusu icin genel referans
baslat_menusu_penceresi = [None]

# --- Acik Pencere Kontrolu ---
def acikmi():
    """Acik uygulama pencerelerinin sinirlarini ve durumunu gunceller."""
    # Listeyi kopyalayarak üzerinde dönmek, remove işlemi sırasında oluşabilecek hataları önler
    for pencere_objesi in list(acik_pencereler):
        if not pencere_objesi.winfo_exists():
            # Pencere kapatilmissa listeden kaldir
            acik_pencereler.remove(pencere_objesi)
        else:
            # Pencere hala aciksa sinirlari guncelle (opsiyonel)
            pencere_objesi.lift()
            pencere_objesi.focus_force()
    pencere.after(100, acikmi) # Her 100 milisaniyede bir kendini tekrar cagir


# --- Yardimci Fonksiyonlar ---
def uzerine_gelince(buton):
    buton.configure(fg_color="#111111")

def uzerinden_ayrilinca(buton):
    buton.configure(fg_color="#000000")

def buton_tiklama_gorseli(buton):
    buton.configure(fg_color="#4f4f4f")
    pencere.after(100, lambda: buton.configure(fg_color="#000000"))

# --- Kendi Kendine Yeterli Ozel Baslik Cubugu ---
def baslik_cubugu_olustur(pencere_referansi, baslik="Pencere"):
    """Suruklenebilir ve kapatma butonlu bir baslik cubugu olusturur."""
    def hareketi_baslat(olay):
        pencere_referansi.x = olay.x
        pencere_referansi.y = olay.y

    def hareket_et(olay):
        x_konumu = pencere_referansi.winfo_pointerx() - pencere_referansi.x
        y_konumu = pencere_referansi.winfo_pointery() - pencere_referansi.y
        pencere_referansi.geometry(f"+{x_konumu}+{y_konumu}")

    def pencereyi_kapat():
        """Varsayilan kapatma komutu."""
        if pencere_referansi in acik_pencereler:
            acik_pencereler.remove(pencere_referansi)
        pencere_referansi.destroy()

    baslik_cubugu = CTkFrame(pencere_referansi, height=35, fg_color="#000000", corner_radius=0)
    baslik_cubugu.pack(side="top", fill="x")

    baslik_cubugu.bind("<Button-1>", hareketi_baslat)
    baslik_cubugu.bind("<B1-Motion>", hareket_et)

    baslik_etiketi = CTkLabel(baslik_cubugu, text=baslik, font=("Arial", 14, "bold"), text_color="#ffffff")
    baslik_etiketi.pack(side="left", padx=15)
    
    kapatma_butonu = CTkButton(baslik_cubugu, text="✕", text_color="#ffffff", hover_color="red", width=30, fg_color="transparent", command=pencereyi_kapat)
    kapatma_butonu.pack(side="right", padx=5, pady=2)

    return baslik_cubugu

# --- Uygulama Fonksiyonlari ---
def _arama_uygulamasini_ac():
    buton_tiklama_gorseli(Arama_butonu)
    pencere_genisligi, pencere_yuksekligi = 600, 400
    x_konumu, y_konumu = (ekran_genisligi - pencere_genisligi) // 2, (ekran_yuksekligi - pencere_yuksekligi) // 2
    
    AramaPenceresi = CTkToplevel(pencere)
    AramaPenceresi.geometry(f"{pencere_genisligi}x{pencere_yuksekligi}+{x_konumu}+{y_konumu}")
    AramaPenceresi.overrideredirect(True)
    AramaPenceresi.transient(pencere)

    Arama_butonu.configure(image=arama_gorseli,border_width=1,border_color="white",fg_color="#111111")
    
    baslik_cubugu_olustur(AramaPenceresi, "Arama")
    
    icerik_cercevesi = CTkFrame(AramaPenceresi, corner_radius=10, fg_color="#ffffff")
    icerik_cercevesi.pack(fill="both", expand=True)
    
    CTkEntry(icerik_cercevesi, placeholder_text="Aramak icin yazin...").pack(pady=20, padx=20, fill="x")
    
    acik_pencereler.append(AramaPenceresi)
    AramaPenceresi.lift()
    AramaPenceresi.focus_force()

def _paint_uygulamasini_ac():
    buton_tiklama_gorseli(Paint_butonu)
    pencere_genisligi, pencere_yuksekligi = 800, 600
    x_konumu, y_konumu = (ekran_genisligi - pencere_genisligi) // 2, (ekran_yuksekligi - pencere_yuksekligi) // 2
    
    PaintPenceresi = CTkToplevel(pencere)
    PaintPenceresi.geometry(f"{pencere_genisligi}x{pencere_yuksekligi}+{x_konumu}+{y_konumu}")
    PaintPenceresi.overrideredirect(True)
    PaintPenceresi.transient(pencere)

    baslik_cubugu_olustur(PaintPenceresi, "Paint")

    Paint_butonu.configure(image=paint_gorseli,border_width=1,border_color="white",fg_color="#111111")

    renkler_cercevesi = CTkFrame(PaintPenceresi, fg_color="#d3d3d3", height=50, corner_radius=0)
    renkler_cercevesi.pack(side="top", fill="x")

    gecerli_renk = {"renk": "black"}
    def rengi_ayarla(renk):
        gecerli_renk["renk"] = renk

    # Renk butonlari
    for renk_kodu in ["blue", "green", "red", "black", "white"]:
        CTkButton(renkler_cercevesi, text="", width=25, height=25, fg_color=renk_kodu, command=lambda r=renk_kodu: rengi_ayarla(r)).pack(side="left", padx=5, pady=5)
    
    # Firca boyutu
    boyut_secimi = CTkComboBox(renkler_cercevesi, values=[str(i) for i in range(2, 21, 2)])
    boyut_secimi.set("4")
    boyut_secimi.pack(side="left", padx=10)

    tuval = Canvas(PaintPenceresi, bg="white", highlightthickness=0)
    tuval.pack(fill="both", expand=True)

    def ciz(olay):
        try:
            cizim_boyutu = int(boyut_secimi.get())
            x1, y1 = (olay.x - cizim_boyutu // 2), (olay.y - cizim_boyutu // 2)
            x2, y2 = (olay.x + cizim_boyutu // 2), (olay.y + cizim_boyutu // 2)
            tuval.create_oval(x1, y1, x2, y2, fill=gecerli_renk["renk"], outline=gecerli_renk["renk"])
        except ValueError: pass

    tuval.bind("<B1-Motion>", ciz)
    acik_pencereler.append(PaintPenceresi)
    PaintPenceresi.lift()
    PaintPenceresi.focus_force()

def _word_uygulamasini_ac():
    buton_tiklama_gorseli(Word_butonu)
    pencere_genisligi, pencere_yuksekligi = 800, 600
    x_konumu, y_konumu = (ekran_genisligi - pencere_genisligi) // 2, (ekran_yuksekligi - pencere_yuksekligi) // 2
    
    WordPenceresi = CTkToplevel(pencere)
    WordPenceresi.geometry(f"{pencere_genisligi}x{pencere_yuksekligi}+{x_konumu}+{y_konumu}")
    WordPenceresi.overrideredirect(True)
    WordPenceresi.transient(pencere)

    baslik_cubugu = baslik_cubugu_olustur(WordPenceresi, "Word")

    Word_butonu.configure(image=word_gorseli,border_width=1,border_color="white",fg_color="#111111")

    metin_kutusu = CTkTextbox(WordPenceresi, fg_color="#ffffff", corner_radius=0, font=("Arial", 16), text_color="black", wrap="word")
    metin_kutusu.pack(fill="both", expand=True)
    metin_kutusu.focus()
    
    def kaydet_ve_kapat():
        metin_icerigi = metin_kutusu.get("1.0", tk.END)
        try:
            with open(METIN_DOSYASI_YOLU, "w", encoding="utf-8") as f:
                json.dump({"metin": metin_icerigi}, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Dosya kaydedilirken hata olustu: {e}")
        if WordPenceresi in acik_pencereler:
            acik_pencereler.remove(WordPenceresi)
        WordPenceresi.destroy()

    # Bu pencereye ozel olarak kapatma butonunun komutunu degistir
    for arac in baslik_cubugu.winfo_children():
        if isinstance(arac, CTkButton):
            arac.configure(command=kaydet_ve_kapat)
    
    WordPenceresi.protocol("WM_DELETE_WINDOW", kaydet_ve_kapat)
    acik_pencereler.append(WordPenceresi)
    WordPenceresi.lift()
    WordPenceresi.focus_force()

    try:
        with open(METIN_DOSYASI_YOLU, "r", encoding="utf-8") as f:
            metin = json.load(f)
            metin_kutusu.insert("1.0", metin["metin"])
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass

def _hesap_makinesi_uygulamasini_ac():
    buton_tiklama_gorseli(HesapMakinesi_butonu)
    pencere_genisligi, pencere_yuksekligi = 400, 500
    x_konumu, y_konumu = (ekran_genisligi - pencere_genisligi) // 2, (ekran_yuksekligi - pencere_yuksekligi) // 2

    HesapMakinesiPenceresi = CTkToplevel(pencere)
    HesapMakinesiPenceresi.geometry(f"{pencere_genisligi}x{pencere_yuksekligi}+{x_konumu}+{y_konumu}")
    HesapMakinesiPenceresi.overrideredirect(True)
    HesapMakinesiPenceresi.transient(pencere)
    
    baslik_cubugu_olustur(HesapMakinesiPenceresi, "Hesap Makinesi")

    HesapMakinesi_butonu.configure(image=hesap_makinesi_gorseli,border_width=1,border_color="white",fg_color="#111111")

    icerik_cercevesi = CTkFrame(HesapMakinesiPenceresi, fg_color="#ffffff")
    icerik_cercevesi.pack(fill="both", expand=True)

    def asagi(event):
        giris2.focus()

    def yukari(event):
        giris1.focus()

    giris1 = CTkEntry(icerik_cercevesi, placeholder_text="Birinci sayı", font=("Arial", 17))
    giris1.pack(pady=10, padx=20, fill="x")
    giris1.bind("<Down>",asagi)
    giris1.bind("<Return>",asagi)
    giris2 = CTkEntry(icerik_cercevesi, placeholder_text="İkinci sayı", font=("Arial", 17))
    giris2.pack(pady=10, padx=20, fill="x")
    giris2.bind("<Up>",yukari)

    etiket_sonuc = CTkLabel(icerik_cercevesi, text="", font=("Arial", 24, "bold"), text_color="#000000")
    etiket_sonuc.pack(pady=20)

    def hesapla(islem):
        try:
            sayi1, sayi2 = float(giris1.get()), float(giris2.get())
            if islem == '+': sonuc = sayi1 + sayi2
            elif islem == '-': sonuc = sayi1 - sayi2
            elif islem == '*': sonuc = sayi1 * sayi2
            elif islem == '**': sonuc = sayi1 ** sayi2
            elif islem == '/': sonuc = "Hata" if sayi2 == 0 else sayi1 / sayi2
            etiket_sonuc.configure(text=f"{sonuc:.4f}" if isinstance(sonuc, float) else str(sonuc))
        except (ValueError, TypeError):
            etiket_sonuc.configure(text="Gecersiz Giris")

    buton_cercevesi = CTkFrame(icerik_cercevesi, fg_color="transparent")
    buton_cercevesi.pack(pady=10)
    buton_stili = {'width': 60, 'height': 60, 'font': ("Arial", 20),"hover_color":"gray"}

    CTkButton(buton_cercevesi,fg_color="white",border_width=1,text_color="black", text="+", command=lambda: hesapla('+'), **buton_stili).grid(row=0, column=0, padx=5, pady=5)
    CTkButton(buton_cercevesi,fg_color="white",border_width=1,text_color="black", text="-", command=lambda: hesapla('-'), **buton_stili).grid(row=0, column=1, padx=5, pady=5)
    CTkButton(buton_cercevesi,fg_color="white",border_width=1,text_color="black", text="×", command=lambda: hesapla('*'), **buton_stili).grid(row=0, column=2, padx=5, pady=5)
    CTkButton(buton_cercevesi,fg_color="white",border_width=1,text_color="black", text="÷", command=lambda: hesapla('/'), **buton_stili).grid(row=1, column=0, padx=5, pady=5)
    CTkButton(buton_cercevesi,fg_color="white",border_width=1,text_color="black", text="x²", command=lambda: hesapla('**'), **buton_stili).grid(row=1, column=1, padx=5, pady=5)

    acik_pencereler.append(HesapMakinesiPenceresi)
    HesapMakinesiPenceresi.lift()
    HesapMakinesiPenceresi.focus_force()
    giris1.focus()

def _ayarlar_uygulamasini_ac():
    pencere_genisligi, pencere_yuksekligi = 900, 700
    x_konumu, y_konumu = (ekran_genisligi - pencere_genisligi) // 2, (ekran_yuksekligi - pencere_yuksekligi) // 2

    Ayarlarpenceresi = CTkToplevel(pencere)
    Ayarlarpenceresi.geometry(f"{pencere_genisligi}x{pencere_yuksekligi}+{x_konumu}+{y_konumu}")
    Ayarlarpenceresi.overrideredirect(True)
    Ayarlarpenceresi.transient(pencere)

    # Ekran fotoğrafı ayarlama fonksiyonu
    def ekran_fotografi_ayarlari():
        dosya_yolu = filedialog.askopenfilename(
            title="Bir Arka Plan Resmi Seçin",
            filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Tüm Dosyalar", "*.*")]
        )
        if dosya_yolu:
            arka_plan_resmi_ayarla(dosya_yolu)
        
    baslik_cubugu = baslik_cubugu_olustur(Ayarlarpenceresi, "Ayarlar")

    icerik_cercevesi = CTkFrame(Ayarlarpenceresi, fg_color="#ffffff")
    icerik_cercevesi.pack(fill="both", expand=True)

    ekran_fotografi_butonu = CTkButton(icerik_cercevesi, text="Ekran Fotoğrafı Değiştir", command=ekran_fotografi_ayarlari)
    ekran_fotografi_butonu.pack(pady=20, padx=20)
    
    # Arka planı sıfırlama butonu
    arka_plan_sifirla_butonu = CTkButton(icerik_cercevesi, text="Arka Planı Sıfırla", command=lambda: arka_plan_resmi_ayarla(None))
    arka_plan_sifirla_butonu.pack(pady=10, padx=20)

    acik_pencereler.append(Ayarlarpenceresi)
    Ayarlarpenceresi.lift()
    Ayarlarpenceresi.focus_force()

# --- Baslat Menusu Fonksiyonu ---
def baslat_menusunu_ac_kapat():
    buton_tiklama_gorseli(MyWin_ana_butonu)
    
    if baslat_menusu_penceresi[0] and baslat_menusu_penceresi[0].winfo_exists():
        baslat_menusu_penceresi[0].destroy()
        baslat_menusu_penceresi[0] = None
        return

    menu_genisligi, menu_yuksekligi = 400, 500
    menu_x = gorev_cubugu_cercevesi.winfo_x() + 0
    menu_y = gorev_cubugu_cercevesi.winfo_y() - menu_yuksekligi - 0
    
    BaslatMenusu = CTkToplevel(pencere)
    baslat_menusu_penceresi[0] = BaslatMenusu
    BaslatMenusu.geometry(f"{menu_genisligi}x{menu_yuksekligi}+0+{menu_y}")
    BaslatMenusu.overrideredirect(True)
    BaslatMenusu.transient(pencere)
    BaslatMenusu.configure(fg_color="#1a1a1a")

    MyWin_ana_butonu.configure(image=mywin_gorseli,border_width=1,border_color="white",fg_color="#111111")

    def uygulamayi_ac(uygulama_fonksiyonu):
        baslat_menusunu_ac_kapat() # Once menuyu kapat
        uygulama_fonksiyonu()      # Sonra uygulamayi ac

    def pencereyi_kapat():
        pencere.destroy()

    try:
        paint_gorseli_menu = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Paint.png")), size=(40, 40))
        word_gorseli_menu = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Word.png")), size=(40, 40))
        hesap_makinesi_gorseli_menu = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Calculator.png")), size=(40, 40))
        ayarlar_gorseli_menu = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Settings.png")), size=(40, 40))

        menu_buton_stili = {"compound": "left", "width": 300, "height": 60, "corner_radius": 15, "fg_color": "#222222", "text_color": "#ffffff", "font": ("Arial", 18, "bold")}
        
        CTkButton(BaslatMenusu, text="Paint", image=paint_gorseli_menu, command=lambda: uygulamayi_ac(_paint_uygulamasini_ac), **menu_buton_stili).pack(pady=20, padx=20)
        CTkButton(BaslatMenusu, text="Word", image=word_gorseli_menu, command=lambda: uygulamayi_ac(_word_uygulamasini_ac), **menu_buton_stili).pack(pady=10, padx=20)
        CTkButton(BaslatMenusu, text="Hesap Makinesi", image=hesap_makinesi_gorseli_menu, command=lambda: uygulamayi_ac(_hesap_makinesi_uygulamasini_ac), **menu_buton_stili).pack(pady=10, padx=20)
        CTkButton(BaslatMenusu, text="Ayarlar", image=ayarlar_gorseli_menu, command=lambda: uygulamayi_ac(_ayarlar_uygulamasini_ac), **menu_buton_stili).pack(pady=10, padx=20)
        CTkButton(BaslatMenusu, text="Uygulamayi Kapat", command=pencereyi_kapat, **menu_buton_stili).pack(pady=20, padx=20)

    except FileNotFoundError as e:
        CTkLabel(BaslatMenusu, text=f"Varlik bulunamadi:\n{e}", text_color="red").pack(pady=20)
    
    BaslatMenusu.lift()
    BaslatMenusu.focus_force()

# --- Görev Çubuğu Butonlarının Kurulumu ---
mywin_gorseli = None
arama_gorseli = None
paint_gorseli = None
word_gorseli = None
hesap_makinesi_gorseli = None

try:
    mywin_gorseli = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "MyWin.png")), size=(30, 30))
    arama_gorseli = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Search.png")), size=(30, 30))
    paint_gorseli = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Paint.png")), size=(30, 30))
    word_gorseli = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Word.png")), size=(30, 30))
    hesap_makinesi_gorseli = CTkImage(Image.open(os.path.join(VARLIK_YOLU, "Calculator.png")), size=(30, 30))

    buton_ayarlari = {"width": 50, "height": 50, "corner_radius": 5, "fg_color": "#000000"}
    
    MyWin_ana_butonu = CTkButton(gorev_cubugu_cercevesi, image=mywin_gorseli, command=baslat_menusunu_ac_kapat, text="", **buton_ayarlari)
    Arama_butonu = CTkButton(gorev_cubugu_cercevesi, image=arama_gorseli, command=_arama_uygulamasini_ac, text="", **buton_ayarlari)
    Paint_butonu = CTkButton(gorev_cubugu_cercevesi, image=paint_gorseli, command=_paint_uygulamasini_ac, text="", **buton_ayarlari)
    Word_butonu = CTkButton(gorev_cubugu_cercevesi, image=word_gorseli, command=_word_uygulamasini_ac, text="", **buton_ayarlari)
    HesapMakinesi_butonu = CTkButton(gorev_cubugu_cercevesi, image=hesap_makinesi_gorseli, command=_hesap_makinesi_uygulamasini_ac, text="", **buton_ayarlari)
    # zaman_butonu zaten yukarıda tanımlandı ve pack edildi

    buton_listesi = [MyWin_ana_butonu, Arama_butonu, Paint_butonu, Word_butonu, HesapMakinesi_butonu]
    for buton in buton_listesi:
        buton.pack(side="left", padx=5, pady=5)
        buton.bind("<Enter>", lambda olay, b=buton: uzerine_gelince(b))
        buton.bind("<Leave>", lambda olay, b=buton: uzerinden_ayrilinca(b))

    # zaman_butonu için zaten yukarıda bind'ler yapıldı
    # zaman_butonu.pack(side="right", padx=5, pady=5) # Zaten yukarıda pack edildi
    # zaman_butonu.bind("<Enter>", lambda olay, b=zaman_butonu: uzerine_gelince(b))
    # zaman_butonu.bind("<Leave>", lambda olay, b=zaman_butonu: uzerinden_ayrilinca(b))

except FileNotFoundError as e:
    CTkLabel(pencere, text=f"KRITIK HATA: Varlik bulunamadi. 'assets' klasorunun dogru yerde oldugundan emin olun.\n{e}", text_color="red").place(relx=0.5, rely=0.5, anchor="center")

# Uygulamanın döngüsü başlamadan önce çağrılar
acikmi()
zamani_guncelle() # İlk kez metni doğru ayarla

pencere.mainloop()