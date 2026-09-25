"""Builds ms/index.html and id/index.html from the English index.html.

Run from the repo root after editing the English page:  python3 tools/i18n.py
Every visible English string must have an entry below; the script fails
loudly on any text it does not know, so a new English line cannot ship
untranslated. Malay and Indonesian are separate translations, not
variants of each other.
"""
import html
import re
import sys

SRC = 'index.html'

T = {
    # English: (Malay, Indonesian)
    "00 · Filed · 25.09.2026": ("00 · Difailkan · 25.09.2026", "00 · Diarsipkan · 25.09.2026"),
    "Until it's done.": ("Sampai siap.", "Sampai selesai."),
    "How it nags": ("Cara ia menggesa", "Cara kerjanya"),
    "Reliability": ("Kebolehpercayaan", "Keandalan"),
    "Pricing": ("Harga", "Harga"),
    "Coming soon": ("Akan datang", "Segera hadir"),
    "Android reminders · Offline · EN / MS / ID": ("Peringatan Android · Luar talian · EN / MS / ID", "Pengingat Android · Offline · EN / MS / ID"),
    "Reminders that ring again until you tap Done.": ("Peringatan yang berdering lagi sehingga anda ketik Selesai.", "Pengingat yang berbunyi lagi sampai kamu ketuk Selesai."),
    'Sampai is Malay and Indonesian for "until". Free for three active reminders. No account, no cloud, no ads.': (
        "Berdering sehingga kerja betul-betul siap. Percuma untuk tiga peringatan aktif. Tiada akaun, tiada awan, tiada iklan.",
        "Terus berbunyi sampai urusan benar-benar beres. Gratis untuk tiga pengingat aktif. Tanpa akun, tanpa cloud, tanpa iklan."),
    "COMING SOON TO": ("AKAN DATANG DI", "SEGERA HADIR DI"),
    "See how it nags": ("Lihat cara ia menggesa", "Lihat cara kerjanya"),
    "Fig. 1": ("Rajah 1", "Gambar 1"),
    "Fig. 2": ("Rajah 2", "Gambar 2"),
    "Alert 4 · Lock screen": ("Amaran 4 · Skrin kunci", "Peringatan 4 · Layar kunci"),
    "Re-alerts every": ("Berdering semula setiap", "Berbunyi lagi setiap"),
    "1–60 min": ("1–60 min", "1–60 mnt"),
    "Account": ("Akaun", "Akun"),
    "None": ("Tiada", "Tidak ada"),
    "Data": ("Data", "Data"),
    "On device": ("Dalam peranti", "Di perangkat"),
    "Free tier": ("Pelan percuma", "Paket gratis"),
    "3 active": ("3 aktif", "3 aktif"),
    "01 · The nag": ("01 · Gesaan", "01 · Pengingat berulang"),
    "It rings. Then it rings again.": ("Ia berdering. Kemudian berdering lagi.", "Berbunyi. Lalu berbunyi lagi."),
    "A reminder fires at its time, then re-alerts every 1, 5, 10, 15, 30 or 60 minutes until you tap Done or reschedule it. It never looks anxious about it.": (
        "Peringatan berbunyi tepat pada masanya, kemudian berdering semula setiap 1, 5, 10, 15, 30 atau 60 minit sehingga anda ketik Selesai atau jadualkan semula. Tenang, tetapi tidak berhenti.",
        "Pengingat berbunyi tepat waktu, lalu berbunyi lagi setiap 1, 5, 10, 15, 30 atau 60 menit sampai kamu ketuk Selesai atau menjadwalkan ulang. Tenang, tapi tidak berhenti."),
    "Done": ("Selesai", "Selesai"),
    "Done after 4 alerts.": ("Selesai selepas 4 amaran.", "Selesai setelah 4 peringatan."),
    "Filed.": ("Difailkan.", "Diarsipkan."),
    "Alert 1 · 09:00 · Every 10 min": ("Amaran 1 · 09:00 · Setiap 10 min", "Peringatan 1 · 09.00 · Setiap 10 mnt"),
    "Alert 2 · 09:10 · Every 10 min": ("Amaran 2 · 09:10 · Setiap 10 min", "Peringatan 2 · 09.10 · Setiap 10 mnt"),
    "Alert 3 · 09:20 · Every 10 min": ("Amaran 3 · 09:20 · Setiap 10 min", "Peringatan 3 · 09.20 · Setiap 10 mnt"),
    "Alert 4 · 09:30 · Every 10 min": ("Amaran 4 · 09:30 · Setiap 10 min", "Peringatan 4 · 09.30 · Setiap 10 mnt"),
    "Create · keyboard up": ("Cipta · papan kekunci sedia", "Buat · keyboard siap"),
    "02 · Five seconds": ("02 · Lima saat", "02 · Lima detik"),
    "Title, one chip, Save.": ("Tajuk, satu cip, Simpan.", "Judul, satu cip, Simpan."),
    "The sheet opens with the keyboard already up. Everything you need sits in thumb reach, so a reminder takes under five seconds to set.": (
        "Helaian dibuka dengan papan kekunci sudah sedia. Semua yang diperlukan dalam jangkauan ibu jari, jadi peringatan siap dalam kurang lima saat.",
        "Lembar terbuka dengan keyboard sudah siap. Semua yang kamu perlukan terjangkau ibu jari, jadi pengingat siap dalam kurang dari lima detik."),
    "Type the title": ("Taip tajuk", "Ketik judul"),
    "Tap a time chip": ("Ketik cip masa", "Ketuk cip waktu"),
    "In 30 min": ("Dalam 30 min", "Dalam 30 mnt"),
    "In 1 h": ("Dalam 1 jam", "Dalam 1 jam"),
    "Tonight 8pm": ("Malam ini 8 mlm", "Malam ini 20.00"),
    "Tomorrow 9am": ("Esok 9 pagi", "Besok 09.00"),
    "Pick the nag, Save": ("Pilih gesaan, Simpan", "Pilih interval, Simpan"),
    "60 min": ("60 min", "60 mnt"),
    "03 · Reliability": ("03 · Kebolehpercayaan", "03 · Keandalan"),
    "9:00 means 9:00. Not 9:07.": ("9:00 bermakna 9:00. Bukan 9:07.", "09.00 berarti 09.00. Bukan 09.07."),
    "Android aggressively kills background apps to save battery, meaning your reminders fail silently. Sampai guides you through the 4 critical permissions that keep alerts active, audits brand-specific quirks, and sends a test ring to prove it works.": (
        "Android agresif mematikan aplikasi latar belakang untuk menjimatkan bateri, jadi peringatan anda gagal tanpa disedari. Sampai membimbing anda melalui 4 kebenaran penting yang memastikan amaran kekal aktif, menyemak kelemahan khusus jenama telefon, dan menghantar deringan ujian untuk membuktikan ia berfungsi.",
        "Android secara agresif mematikan aplikasi latar belakang demi menghemat baterai, sehingga pengingatmu gagal diam-diam. Sampai memandumu melalui 4 izin penting yang menjaga peringatan tetap aktif, memeriksa kendala khusus tiap merek, dan mengirim dering uji untuk membuktikan semuanya bekerja."),
    "Notifications": ("Pemberitahuan", "Notifikasi"),
    "Ensures your reminders make sound and appear in the drawer.": ("Memastikan peringatan anda berbunyi dan muncul di laci pemberitahuan.", "Memastikan pengingat berbunyi dan muncul di panel notifikasi."),
    "Not set": ("Belum", "Belum"),
    "OK": ("OK", "OK"),
    "Alarms & Reminders": ("Penggera & Peringatan", "Alarm & Pengingat"),
    "Bypasses system throttling so alerts trigger down to the exact second.": ("Memintas sekatan sistem supaya amaran berbunyi tepat hingga ke saat.", "Melewati pembatasan sistem sehingga peringatan berbunyi tepat sampai ke detik."),
    "Full-Screen Alerts": ("Amaran Skrin Penuh", "Notifikasi Layar Penuh"),
    "Wakes your display and demands attention, exactly like a real alarm.": ("Menghidupkan skrin dan menuntut perhatian, sama seperti jam loceng sebenar.", "Menyalakan layar dan menuntut perhatian, persis seperti alarm sungguhan."),
    "Unrestricted Battery": ("Bateri Tanpa Had", "Baterai Tanpa Batasan"),
    "Prevents Android from putting Sampai to sleep. The #1 cause of missed alerts.": ("Menghalang Android daripada menidurkan Sampai. Punca utama amaran terlepas.", "Mencegah Android menidurkan Sampai. Penyebab utama peringatan terlewat."),
    "Built for Android's fragmentation.": ("Dibina untuk kepelbagaian Android.", "Dibuat untuk keragaman Android."),
    "Automatically detects aggressive background-killing on Samsung, Xiaomi, OPPO, vivo, OnePlus, and Honor, taking you directly to the hidden switches to fix them.": (
        "Mengesan secara automatik aplikasi yang dimatikan secara agresif pada Samsung, Xiaomi, OPPO, vivo, OnePlus dan Honor, dan membawa anda terus ke suis tersembunyi untuk membetulkannya.",
        "Otomatis mendeteksi pematian aplikasi yang agresif di Samsung, Xiaomi, OPPO, vivo, OnePlus, dan Honor, lalu membawamu langsung ke sakelar tersembunyi untuk memperbaikinya."),
    "Test · Ring me in 10 seconds. Lock your phone.": ("Ujian · Deringkan saya dalam 10 saat. Kunci telefon anda.", "Uji · Bunyikan dalam 10 detik. Kunci ponselmu."),
    "Seconds": ("Saat", "Detik"),
    "Passed. Sampai can wake this phone.": ("Lulus. Sampai boleh membangunkan telefon ini.", "Lulus. Sampai bisa membangunkan ponsel ini."),
    "Every screen, filed.": ("Setiap skrin, difailkan.", "Setiap layar, diarsipkan."),
    "04 · Scroll →": ("04 · Tatal →", "04 · Gulir →"),
    "Onboarding": ("Permulaan", "Pengenalan"),
    "Four permissions, each with one plain sentence.": ("Empat kebenaran, setiap satu dengan satu ayat mudah.", "Empat izin, masing-masing dengan satu kalimat sederhana."),
    "Rings you in 10 seconds to prove it works.": ("Berdering dalam 10 saat untuk membuktikan ia berfungsi.", "Berbunyi dalam 10 detik untuk membuktikan semuanya bekerja."),
    "Home": ("Utama", "Beranda"),
    "Overdue first. Swipe right for Done, left for Snooze.": ("Yang lewat di atas. Leret ke kanan untuk Selesai, ke kiri untuk Tunda.", "Yang terlambat di atas. Geser ke kanan untuk Selesai, ke kiri untuk Tunda."),
    "Alert": ("Amaran", "Peringatan"),
    "Takes over the lock screen like an alarm clock.": ("Mengambil alih skrin kunci seperti jam loceng.", "Mengambil alih layar kunci seperti jam alarm."),
    "History": ("Sejarah", "Riwayat"),
    "Done items rest here for 30 days.": ("Item selesai disimpan di sini selama 30 hari.", "Item selesai disimpan di sini selama 30 hari."),
    "Widgets": ("Widget", "Widget"),
    "Next up and Upcoming on the home screen. Pro.": ("Seterusnya dan Akan datang di skrin utama. Pro.", "Berikutnya dan Akan datang di layar utama. Pro."),
    "Settings": ("Tetapan", "Setelan"),
    "Export to a plain file. Import it back.": ("Eksport ke fail biasa. Import semula.", "Ekspor ke file biasa. Impor kembali."),
    "05 · What it does not do": ("05 · Apa yang ia tidak buat", "05 · Yang tidak dilakukannya"),
    "No account.": ("Tiada akaun.", "Tanpa akun."),
    "Open it and start": ("Buka dan terus guna", "Buka dan langsung pakai"),
    "No cloud.": ("Tiada awan.", "Tanpa cloud."),
    "Stored on this phone": ("Disimpan dalam telefon ini", "Disimpan di ponsel ini"),
    "No ads.": ("Tiada iklan.", "Tanpa iklan."),
    "Paid for by Pro, not by you": ("Dibiayai Pro, bukan perhatian anda", "Dibiayai Pro, bukan perhatianmu"),
    "No AI.": ("Tiada AI.", "Tanpa AI."),
    "It rings. That is the job": ("Ia berdering. Itu tugasnya", "Berbunyi. Itu tugasnya"),
    "No streaks.": ("Tiada streak.", "Tanpa streak."),
    "Nothing to keep up": ("Tiada apa untuk dikejar", "Tidak ada yang harus dikejar"),
    "Nothing leaves the device.": ("Tiada apa yang keluar dari peranti.", "Tidak ada yang keluar dari perangkat."),
    "06 · Pricing": ("06 · Harga", "06 · Harga"),
    "Everything that makes a reminder ring stays free.": ("Semua yang membuat peringatan berdering kekal percuma.", "Semua yang membuat pengingat berbunyi tetap gratis."),
    "Free": ("Percuma", "Gratis"),
    "RM0": ("RM0", "RM0"),
    "3 active reminders": ("3 peringatan aktif", "3 pengingat aktif"),
    "Nag every 1 to 60 min": ("Gesa setiap 1 hingga 60 min", "Ulang setiap 1 sampai 60 mnt"),
    "Full-screen alerts": ("Amaran skrin penuh", "Notifikasi layar penuh"),
    "Reliability check": ("Semakan kebolehpercayaan", "Cek keandalan"),
    "Everything that makes a reminder ring.": ("Semua yang membuat peringatan berdering.", "Semua yang membuat pengingat berbunyi."),
    "Yearly": ("Tahunan", "Tahunan"),
    "Pro": ("Pro", "Pro"),
    "RM19.90": ("RM19.90", "RM19.90"),
    "/ year": ("/ tahun", "/ tahun"),
    "Unlimited reminders": ("Peringatan tanpa had", "Pengingat tanpa batas"),
    "Home-screen widgets": ("Widget skrin utama", "Widget layar utama"),
    "Unlimited history": ("Sejarah tanpa had", "Riwayat tanpa batas"),
    "Renews yearly. Cancel in Play any time.": ("Diperbaharui setiap tahun. Batal di Play bila-bila masa.", "Diperpanjang tiap tahun. Batalkan di Play kapan saja."),
    "Lifetime": ("Seumur hidup", "Seumur hidup"),
    "RM49.90": ("RM49.90", "RM49.90"),
    "once": ("sekali", "sekali"),
    "Everything in Pro": ("Semua dalam Pro", "Semua fitur Pro"),
    "Paid once": ("Bayar sekali", "Bayar sekali"),
    "Unlocked forever": ("Dibuka selamanya", "Terbuka selamanya"),
    "One purchase, tied to your Play account.": ("Satu pembelian, terikat pada akaun Play anda.", "Satu pembelian, terikat ke akun Play-mu."),
    "Malaysian prices. Google Play shows the price for your country.": ("Harga Malaysia. Google Play memaparkan harga untuk negara anda.", "Harga dalam ringgit Malaysia. Google Play menampilkan harga dalam mata uang negaramu."),
    "HONOURED FOREVER.": ("DIHORMATI SELAMANYA.", "DIJAMIN SELAMANYA."),
    "If this app ever leaves the Play Store or changes hands, your purchase stays unlocked in the last version shipped. Your data exports to a plain file from Settings, today and always. No account. Nothing leaves your phone except the receipt Google Play needs.": (
        "Jika aplikasi ini meninggalkan Play Store atau bertukar tangan, pembelian anda kekal dibuka dalam versi terakhir yang dikeluarkan. Data anda boleh dieksport ke fail biasa dari Tetapan, hari ini dan selamanya. Tiada akaun. Tiada apa yang keluar dari telefon anda kecuali resit yang diperlukan Google Play.",
        "Jika aplikasi ini keluar dari Play Store atau berpindah tangan, pembelianmu tetap terbuka di versi terakhir yang dirilis. Datamu bisa diekspor ke file biasa dari Setelan, hari ini dan selamanya. Tanpa akun. Tidak ada yang keluar dari ponselmu kecuali tanda terima yang diperlukan Google Play."),
    "07 · English · Bahasa Melayu · Bahasa Indonesia": ("07 · English · Bahasa Melayu · Bahasa Indonesia", "07 · English · Bahasa Melayu · Bahasa Indonesia"),
    "Sampai siap.": ("Sampai siap.", "Sampai siap."),
    "Sampai selesai.": ("Sampai selesai.", "Sampai selesai."),
    "Coming soon to Google Play": ("Akan datang di Google Play", "Segera hadir di Google Play"),
    "Until": ("Berdering", "Berbunyi"),
    "it's": ("sampai", "sampai"),
    "done.": ("siap.", "selesai."),
    "Android · No account · Nothing leaves the device": ("Android · Tiada akaun · Tiada apa keluar dari peranti", "Android · Tanpa akun · Tidak ada yang keluar dari perangkat"),
    "© 2026 Sampai": ("© 2026 Sampai", "© 2026 Sampai"),
    "Privacy": ("Privasi", "Privasi"),
    "Terms": ("Terma", "Ketentuan"),
    "Contact": ("Hubungi", "Kontak"),
    # Side-label section names (data-sec) and image alt text.
    "04 · Every screen": ("04 · Setiap skrin", "04 · Setiap layar"),
    "07 · Three languages": ("07 · Tiga bahasa", "07 · Tiga bahasa"),
    "08 · Get it": ("08 · Dapatkan", "08 · Dapatkan"),
    "Sampai alert on the lock screen: a large numeral 4, the reminder Call Mak about Sunday lunch, and Done, Snooze and Reschedule buttons.": (
        "Amaran Sampai di skrin kunci: angka 4 yang besar, peringatan Call Mak about Sunday lunch, dan butang Selesai, Tunda dan Jadual semula.",
        "Peringatan Sampai di layar kunci: angka 4 besar, pengingat Call Mak about Sunday lunch, dan tombol Selesai, Tunda, dan Jadwalkan ulang."),
    "The new reminder sheet with time chips, nag interval chips from 1 to 60 minutes and a Save button.": (
        "Helaian peringatan baharu dengan cip masa, cip selang gesaan dari 1 hingga 60 minit dan butang Simpan.",
        "Lembar pengingat baru dengan cip waktu, cip interval 1 sampai 60 menit, dan tombol Simpan."),
}

# Strings that are the same in every language and need no entry.
SAME = {"SAMPAI", "S", "a", "m", "p", "i", "Google Play", "sampai", "Sampai", "EN", "MS", "ID"}

META = {
    'ms': dict(lang='ms', title='Sampai: peringatan yang berdering sehingga siap',
               desc='Sampai ialah aplikasi peringatan Android yang berdering semula setiap 1, 5, 10, 15, 30 atau 60 minit sehingga anda ketik Selesai. Luar talian, tiada akaun, tiada iklan.',
               swipe='Leret'),
    'id': dict(lang='id', title='Sampai: pengingat yang berbunyi sampai selesai',
               desc='Sampai adalah aplikasi pengingat Android yang berbunyi lagi setiap 1, 5, 10, 15, 30 atau 60 menit sampai kamu ketuk Selesai. Offline, tanpa akun, tanpa iklan.',
               swipe='Geser'),
}


def lookup(text, idx):
    if text in SAME:
        return text
    if re.fullmatch(r'[\d:.·↓→!/ –-]+', text) or re.fullmatch(r'0\d|\d\d?', text):
        return text
    entry = T.get(text)
    if entry is None:
        sys.exit(f'No translation for: {text!r}')
    return entry[idx]


def switcher(active, prefix):
    links = []
    for code, href in (('EN', prefix or './'), ('MS', prefix + 'ms/'), ('ID', prefix + 'id/')):
        weight = 'color:rgb(var(--i))' if code == active else 'color:rgba(var(--i),.5)'
        cur = ' aria-current="page"' if code == active else ''
        links.append(f'<a href="{href}" hreflang="{code.lower()}"{cur} style="text-decoration:none;{weight}">{code}</a>')
    return '<span data-langs="" style="display:flex;gap:10px">' + ''.join(links) + '</span>'


def alternates(prefix):
    return ''.join(f'<link rel="alternate" hreflang="{h}" href="https://haziqlucii.github.io/sampai-site/{p}">\n'
                   for h, p in (('en', ''), ('ms', 'ms/'), ('id', 'id/')))


def add_switcher(page, active, prefix):
    page = re.sub(r'<span data-langs=""[^>]*>(?:<a [^>]*>[A-Z]{2}</a>)+</span>', '', page)
    anchor = '<a href="#get" style="height:34px'
    assert page.count(anchor) == 1
    page = page.replace(anchor, switcher(active, prefix) + anchor, 1)
    page = re.sub(r'<link rel="alternate" hreflang[^>]*>\n', '', page)
    page = page.replace('<link rel="icon"', alternates(prefix) + '<link rel="icon"', 1)
    return page


def build(lang, idx):
    page = open(SRC).read()
    page = add_switcher(page, lang.upper(), '../')
    head, body = page.split('<body>', 1)
    body_html, scripts = body.split('<script src=', 1)

    def text_node(m):
        raw = m.group(1)
        stripped = html.unescape(raw).strip()
        if not stripped:
            return m.group(0)
        lead = raw[:len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        out = lookup(stripped, idx)
        if lang == 'id' and re.fullmatch(r'\d\d:\d\d', out):
            out = out.replace(':', '.')
        return '>' + lead + html.escape(out, quote=False) + trail + '<'

    mq_start = body_html.index('<div data-mq=""')
    mq_end = body_html.index('</section>', mq_start)
    marquee = body_html[mq_start:mq_end]
    body_html = body_html[:mq_start] + '<i data-mq-slot=""></i>' + body_html[mq_end:]
    body_html = re.sub(r'>([^<>]+)<', text_node, body_html)
    body_html = body_html.replace('<i data-mq-slot=""></i>', marquee)

    def attr(m):
        name, value = m.group(1), m.group(2)
        text = html.unescape(value)
        if name == 'data-sec' or name == 'alt' or name == 'aria-label':
            if name == 'alt' and ' screen. ' in text:
                title, desc = text.split(' screen. ', 1)
                t = lookup(title, idx)
                d = lookup(desc, idx)
                return f'{name}="{html.escape(t + ": " + d)}"'
            return f'{name}="{html.escape(lookup(text, idx))}"'
        return m.group(0)

    body_html = re.sub(r'\b(data-sec|alt|aria-label)="([^"]*)"', attr, body_html)
    body_html = body_html.replace('href="privacy/"', 'href="../privacy/"').replace('href="terms/"', 'href="../terms/"')
    body_html = body_html.replace('src="assets/', 'src="../assets/')
    scripts = scripts.replace('"assets/', '"../assets/')

    meta = META[lang]
    head = head.replace('<html lang="en">', f'<html lang="{meta["lang"]}">')
    head = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + meta['desc'], head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + meta['title'], head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + meta['desc'], head)
    head = head.replace('content="assets/', 'content="../assets/').replace('href="assets/', 'href="../assets/')
    head = head.replace('content: "Swipe \\2192"', f'content: "{meta["swipe"]} \\2192"')
    return head + '<body>' + body_html + '<script src=' + scripts


if __name__ == '__main__':
    en = add_switcher(open(SRC).read(), 'EN', '')
    open(SRC, 'w').write(en)
    import os
    for lang, idx in (('ms', 0), ('id', 1)):
        os.makedirs(lang, exist_ok=True)
        open(f'{lang}/index.html', 'w').write(build(lang, idx))
        print('wrote', f'{lang}/index.html')
