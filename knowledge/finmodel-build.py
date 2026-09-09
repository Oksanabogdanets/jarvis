from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

wb = Workbook()
F = "Arial"
BLUE = Font(name=F, color="0000FF", size=11)
BLACK = Font(name=F, color="000000", size=11)
GREEN = Font(name=F, color="008000", size=11)
BOLD = Font(name=F, bold=True, size=11)
H1 = Font(name=F, bold=True, size=14)
H2 = Font(name=F, bold=True, size=11, color="FFFFFF")
GREY = Font(name=F, size=10, color="666666", italic=True)
YELLOW = PatternFill("solid", fgColor="FFFF00")
DARK = PatternFill("solid", fgColor="1A1A1A")
LIGHT = PatternFill("solid", fgColor="F3E9D7")
thin = Side(style="thin", color="CCCCCC")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
UAH = '#,##0" грн";(#,##0" грн");"-"'
USD = '"$"#,##0;("$"#,##0);"-"'
PCT = '0%'
NUM = '#,##0;(#,##0);"-"'
DEC = '0.0'

def head(ws, row, text, width=None):
    c = ws.cell(row=row, column=1, value=text); c.font = H2; c.fill = DARK
    for col in range(2, 6):
        ws.cell(row=row, column=col).fill = DARK

def inp(ws, row, label, value, fmt=None, note=None, fill=True):
    ws.cell(row=row, column=1, value=label).font = BLACK
    c = ws.cell(row=row, column=2, value=value); c.font = BLUE
    if fill: c.fill = YELLOW
    if fmt: c.number_format = fmt
    if note: ws.cell(row=row, column=3, value=note).font = GREY
    return c

def fml(ws, row, col, label, formula, fmt=None, bold=False, font=None):
    if label is not None:
        ws.cell(row=row, column=1, value=label).font = BOLD if bold else BLACK
    c = ws.cell(row=row, column=col, value=formula)
    c.font = font or (Font(name=F, bold=True, size=11) if bold else BLACK)
    if fmt: c.number_format = fmt
    return c

# ---------------- Вхідні ----------------
ws = wb.active; ws.title = "Вхідні"
ws.column_dimensions["A"].width = 46; ws.column_dimensions["B"].width = 16; ws.column_dimensions["C"].width = 70
ws["A1"] = "ВХІДНІ ДАНІ — усе, що треба заповнити, тут"; ws["A1"].font = H1
ws["A2"] = "Синій текст на жовтому — заповнюєш своїми цифрами. Чорний на інших аркушах — формули, не чіпати. Зелений — посилання на цей аркуш."; ws["A2"].font = GREY

head(ws, 3, "ПАКЕТ І ЦІНА")
inp(ws, 4, "Ціна пакета зараз, грн/міс", 25000, UAH, "ПРИПУЩЕННЯ — постав свою реальну ціну пакета на 15 роликів")
inp(ws, 5, "Роликів у пакеті на місяць", 15, NUM, "Твій пакет: 15 роликів (є ще 30+)")
inp(ws, 6, "Каруселей на місяць", 8, NUM, "ПРИПУЩЕННЯ — скільки каруселей робить Валерія на клієнта")
inp(ws, 7, "Ціна пакета — ціль, грн/міс", 35000, UAH, "Ціль після переходу на «ведення напряму». Ринок: ведення TikTok від 11 000, просування від 25 000 грн/міс (marketing.if.ua)")
inp(ws, 8, "Роликів у пакеті — ціль", 10, NUM, "Ведення продає результат, а не штуки. Менше роликів + стратегія + CTA = вища маржа")

head(ws, 9, "СОБІВАРТІСТЬ НА ОДИНИЦЮ (готівка, підряд)")
inp(ws, 10, "Зйомка, грн за ролик (оператор або студія)", 750, UAH, "Ринок Київ: 2 300 грн/год + студія 700 грн/год, 4 відео за годину (pudraphotostudio.com). Постав, скільки платиш оператору")
inp(ws, 11, "Монтаж, грн за ролик", 450, UAH, "Ринок: 400 грн веб-студія (ifish.com.ua), від 500 фриланс (kabanchik.ua). Постав свою ставку монтажеру")
inp(ws, 12, "Карусель, грн за штуку (Валерія)", 300, UAH, "ПРИПУЩЕННЯ — постав, скільки платиш Валерії")

head(ws, 14, "ЧАС ОКСАНИ НА ОДНОГО КЛІЄНТА НА МІСЯЦЬ")
inp(ws, 15, "Годин — зараз (сама знімаєш і ведеш)", 25, NUM, "ПРИПУЩЕННЯ — порахуй за один тиждень і постав реальне")
inp(ws, 16, "Годин — з режисером-менеджером зйомок", 12, NUM, "Лишаються стратегія, сценарії, комунікація з клієнтом")
inp(ws, 17, "Годин — з режисером і project-менеджером", 6, NUM, "Лишаються стратегія і контроль")
inp(ws, 18, "Скільки має коштувати година Оксани, грн", 800, UAH, "ПРИПУЩЕННЯ — твоя цільова ставка як власника, не як оператора")

head(ws, 20, "КОМАНДА В ШТАТ (фіксовано на місяць)")
inp(ws, 21, "Режисер-менеджер зйомок, грн/міс", 35000, UAH, "Ostrovskyi Team наймає за 30 000–40 000 грн, Київ (Work.ua)")
inp(ws, 22, "Project manager, грн/міс", 50000, UAH, "Ostrovskyi Team: 45 000–60 000 грн, дистанційно (Work.ua)")

head(ws, 24, "РЕКЛАМА І ВОРОНКА")
inp(ws, 25, "Курс долара, грн", 41.5, DEC, "ПРИПУЩЕННЯ — постав актуальний")
inp(ws, 26, "Бюджет реклами, USD на місяць", 250, USD, "Твоя історична норма $130–320/міс (target-osnovy.md). При $8/день кампанія не виходить з навчання — треба $25–30/день")
inp(ws, 27, "Переписок на місяць з реклами", 40, NUM, "Твоя історична норма 25–65 переписок/міс (target-osnovy.md)")
inp(ws, 28, "Частка переписок → зум (заявка)", 0.25, PCT, "ПРИПУЩЕННЯ — постав реальну: скільки з тих, хто написав, дійшли до зуму")
inp(ws, 29, "Частка зумів → угода", 0.30, PCT, "ПРИПУЩЕННЯ — постав реальну конверсію зуму в оплату")
inp(ws, 30, "Середня тривалість клієнта, місяців", 3, NUM, "ПРИПУЩЕННЯ — скільки місяців у середньому клієнт платить")

head(ws, 32, "ПОДАТКИ (ФОП 3 група)")
inp(ws, 33, "Єдиний податок, % від доходу", 0.05, PCT, "5% для 3 групи без ПДВ. Перевір свою групу")
inp(ws, 34, "ЄСВ, грн/міс", 1760, UAH, "22% від мінімальної зарплати. ПРИПУЩЕННЯ — перевір актуальну суму")

head(ws, 36, "КІЛЬКІСТЬ КЛІЄНТІВ ПО СЦЕНАРІЯХ")
inp(ws, 37, "Зараз", 4, NUM, "Діана, Ілона, Каріна, Ольга")
inp(ws, 38, "Крок 1 — через 1–2 місяці", 6, NUM, "З режисером-менеджером зйомок")
inp(ws, 39, "Ціль — через 3 місяці", 10, NUM, "Ціль з GOALS.md: 10 клієнтів на рілс під ключ")

# ---------------- Юніт ----------------
u = wb.create_sheet("Юніт")
u.column_dimensions["A"].width = 44; u.column_dimensions["B"].width = 18; u.column_dimensions["C"].width = 18; u.column_dimensions["D"].width = 60
u["A1"] = "ЮНІТ-ЕКОНОМІКА — один клієнт за один місяць"; u["A1"].font = H1
u["A2"] = "Скільки клієнт приносить, скільки з'їдає підряд, і скільки лишається на годину твого часу"; u["A2"].font = GREY
for col, t in ((2, "Зараз"), (3, "Ціль")):
    c = u.cell(row=3, column=col, value=t); c.font = H2; c.fill = DARK
u.cell(row=3, column=1).fill = DARK
fml(u, 4, 2, "Дохід з клієнта, грн/міс", "=Вхідні!B4", UAH, font=GREEN); fml(u, 4, 3, None, "=Вхідні!B7", UAH, font=GREEN)
fml(u, 5, 2, "Зйомка", "=Вхідні!$B$5*Вхідні!$B$10", UAH); fml(u, 5, 3, None, "=Вхідні!$B$8*Вхідні!$B$10", UAH)
fml(u, 6, 2, "Монтаж", "=Вхідні!$B$5*Вхідні!$B$11", UAH); fml(u, 6, 3, None, "=Вхідні!$B$8*Вхідні!$B$11", UAH)
fml(u, 7, 2, "Каруселі", "=Вхідні!$B$6*Вхідні!$B$12", UAH); fml(u, 7, 3, None, "=Вхідні!$B$6*Вхідні!$B$12", UAH)
fml(u, 8, 2, "Собівартість підряду", "=SUM(B5:B7)", UAH, bold=True); fml(u, 8, 3, None, "=SUM(C5:C7)", UAH, bold=True)
fml(u, 9, 2, "Валова маржа", "=B4-B8", UAH, bold=True); fml(u, 9, 3, None, "=C4-C8", UAH, bold=True)
fml(u, 10, 2, "Валова маржа, %", "=IF(B4=0,0,B9/B4)", PCT); fml(u, 10, 3, None, "=IF(C4=0,0,C9/C4)", PCT)
fml(u, 12, 2, "Години Оксани на клієнта", "=Вхідні!B15", NUM, font=GREEN); fml(u, 12, 3, None, "=Вхідні!B17", NUM, font=GREEN)
fml(u, 13, 2, "Вартість часу Оксани за її ставкою", "=B12*Вхідні!$B$18", UAH); fml(u, 13, 3, None, "=C12*Вхідні!$B$18", UAH)
fml(u, 14, 2, "Маржа після оплати часу Оксани", "=B9-B13", UAH, bold=True); fml(u, 14, 3, None, "=C9-C13", UAH, bold=True)
fml(u, 16, 2, "Скільки клієнт платить за годину Оксани", "=IF(B12=0,0,B9/B12)", UAH, bold=True); fml(u, 16, 3, None, "=IF(C12=0,0,C9/C12)", UAH, bold=True)
u["D16"] = "Порівняй із Вхідні!B18. Якщо менше — ти працюєш дешевше за власну ставку"; u["D16"].font = GREY
u["D8"] = "Це те, що клієнт може порахувати сам по kabanchik.ua. Тому «15 роликів» як одиниця — програшний якір"; u["D8"].font = GREY
u["D14"] = "Якщо тут мінус — пакет збитковий з урахуванням твого часу"; u["D14"].font = GREY

# ---------------- Місяць ----------------
m = wb.create_sheet("Місяць")
m.column_dimensions["A"].width = 44
for col in "BCD": m.column_dimensions[col].width = 18
m.column_dimensions["E"].width = 56
m["A1"] = "МІСЯЦЬ АГЕНЦІЇ — три сценарії"; m["A1"].font = H1
m["A2"] = "Зараз: сама знімаєш. Крок 1: режисер-менеджер зйомок у штаті. Ціль: режисер + project-менеджер, ціна пакета підвищена"; m["A2"].font = GREY
for col, t in ((2, "Зараз"), (3, "Крок 1"), (4, "Ціль")):
    c = m.cell(row=3, column=col, value=t); c.font = H2; c.fill = DARK
m.cell(row=3, column=1).fill = DARK
fml(m, 4, 2, "Клієнтів", "=Вхідні!B37", NUM, font=GREEN); fml(m, 4, 3, None, "=Вхідні!B38", NUM, font=GREEN); fml(m, 4, 4, None, "=Вхідні!B39", NUM, font=GREEN)
fml(m, 5, 2, "Ціна пакета, грн/міс", "=Вхідні!B4", UAH, font=GREEN); fml(m, 5, 3, None, "=Вхідні!B4", UAH, font=GREEN); fml(m, 5, 4, None, "=Вхідні!B7", UAH, font=GREEN)
for col in "BCD":
    fml(m, 6, "BCD".index(col)+2, "ДОХІД", f"={col}4*{col}5", UAH, bold=True)
    fml(m, 7, "BCD".index(col)+2, "Собівартість підряду на клієнта", "=Юніт!$C$8" if col=="D" else "=Юніт!$B$8", UAH, font=GREEN)
    fml(m, 8, "BCD".index(col)+2, "Собівартість підряду всього", f"={col}4*{col}7", UAH)
    fml(m, 9, "BCD".index(col)+2, "Валова маржа", f"={col}6-{col}8", UAH, bold=True)
fml(m, 11, 2, "Режисер-менеджер зйомок", 0, UAH, font=BLUE); fml(m, 11, 3, None, "=Вхідні!B21", UAH, font=GREEN); fml(m, 11, 4, None, "=Вхідні!B21", UAH, font=GREEN)
fml(m, 12, 2, "Project manager", 0, UAH, font=BLUE); fml(m, 12, 3, None, 0, UAH, font=BLUE); fml(m, 12, 4, None, "=Вхідні!B22", UAH, font=GREEN)
for col in "BCD":
    i = "BCD".index(col)+2
    fml(m, 13, i, "Реклама, грн", "=Вхідні!$B$26*Вхідні!$B$25", UAH, font=GREEN)
    fml(m, 14, i, "Постійні витрати всього", f"=SUM({col}11:{col}13)", UAH, bold=True)
    fml(m, 15, i, "Результат до податків", f"={col}9-{col}14", UAH, bold=True)
    fml(m, 16, i, "Єдиний податок", f"={col}6*Вхідні!$B$33", UAH)
    fml(m, 17, i, "ЄСВ", "=Вхідні!$B$34", UAH, font=GREEN)
    fml(m, 18, i, "ПРИБУТОК ОКСАНИ", f"={col}15-{col}16-{col}17", UAH, bold=True)
    fml(m, 19, i, "Чиста маржа, %", f"=IF({col}6=0,0,{col}18/{col}6)", PCT)
fml(m, 21, 2, "Годин Оксани на місяць", "=B4*Вхідні!B15", NUM, font=GREEN); fml(m, 21, 3, None, "=C4*Вхідні!B16", NUM, font=GREEN); fml(m, 21, 4, None, "=D4*Вхідні!B17", NUM, font=GREEN)
for col in "BCD":
    i = "BCD".index(col)+2
    fml(m, 22, i, "Прибуток на годину Оксани", f"=IF({col}21=0,0,{col}18/{col}21)", UAH, bold=True)
m["E18"] = "Це те, що реально доходить до тебе після підряду, команди, реклами й податків"; m["E18"].font = GREY
m["E21"] = "160 годин = повний робочий місяць. Більше — це не бізнес, це перевантаження"; m["E21"].font = GREY
m["E22"] = "Порівняй із Вхідні!B18. Мета — щоб з кожним кроком ця цифра росла"; m["E22"].font = GREY
for r in (18,): 
    for col in "BCD":
        m[f"{col}{r}"].fill = LIGHT

# ---------------- Клієнти ----------------
k = wb.create_sheet("Клієнти")
cols = ["Клієнт", "Ніша", "Пакет", "Ціна, грн/міс", "Роликів/міс", "Старт", "День оплати", "Статус", "Відповідальний", "CTA / куди веде відео", "Результат за місяць", "Нотатки"]
widths = [16, 18, 14, 14, 12, 12, 12, 12, 16, 26, 24, 30]
k["A1"] = "КЛІЄНТИ — трекер"; k["A1"].font = H1
k["A2"] = "Заповни жовті. Рядок «Разом» рахує місячний дохід (MRR) сам. Статус: активний / пауза / завершено"; k["A2"].font = GREY
for i, (c, w) in enumerate(zip(cols, widths), start=1):
    cell = k.cell(row=4, column=i, value=c); cell.font = H2; cell.fill = DARK; cell.alignment = Alignment(wrap_text=True, vertical="center")
    k.column_dimensions[get_column_letter(i)].width = w
k.row_dimensions[4].height = 32
rows = [
    ["Діана", "", "", None, None, "", "", "активний", "Оксана", "", "", "каруселі + відео → Валерія"],
    ["Ілона", "", "", None, None, "", "", "активний", "Оксана", "", "", "вирішити студію та дату зйомки"],
    ["Каріна", "", "", None, None, "", "", "активний", "Оксана", "", "", ""],
    ["Ольга", "нутриціолог", "", None, None, "", "", "активний", "Оксана", "", "", "підкоригувати стратегію"],
    ["Приклад: Клініка N", "стоматологія", "15 роликів", 25000, 15, "01.10.2026", "1", "активний", "Оксана", "«пиши КЛЮЧ» → Direct", "12 заявок, 3 записи", "приклад рядка — видалити"],
]
for r, row in enumerate(rows, start=5):
    for c, v in enumerate(row, start=1):
        cell = k.cell(row=r, column=c, value=v); cell.font = BLUE; cell.border = BOX
        if c in (4,): cell.number_format = UAH
        if c in (2,3,4,5,6,7,10,11) and r < 9: cell.fill = YELLOW
tr = 5 + len(rows) + 1
k.cell(row=tr, column=1, value="РАЗОМ (MRR)").font = BOLD
c = k.cell(row=tr, column=4, value=f"=SUM(D5:D{tr-2})"); c.font = BOLD; c.number_format = UAH
c = k.cell(row=tr, column=5, value=f"=SUM(E5:E{tr-2})"); c.font = BOLD; c.number_format = NUM
c = k.cell(row=tr, column=3, value=f'=COUNTIF(H5:H{tr-2},"активний")'); c.font = BOLD
k.cell(row=tr, column=2, value="активних:").font = GREY
k.cell(row=tr+2, column=1, value="Правило: один клієнт — один рядок. Оплата не прийшла в «День оплати» → статус «пауза», і зйомка не планується.").font = GREY

# ---------------- Реклама ----------------
a = wb.create_sheet("Реклама")
acols = ["Місяць", "Бюджет, USD", "Витрачено, USD", "Переписки", "Зуми (заявки)", "Угоди", "Вартість переписки, USD", "Вартість зуму, USD", "Вартість клієнта, USD", "Нотатки"]
awidths = [18, 12, 14, 12, 14, 10, 20, 18, 20, 40]
a["A1"] = "РЕКЛАМА — місяць за місяцем"; a["A1"].font = H1
a["A2"] = "Заповнюєш перші шість колонок, решта рахується. Рахуй заявкою тільки те, що дійшло до зуму — не переписку (target-osnovy.md)"; a["A2"].font = GREY
for i, (c, w) in enumerate(zip(acols, awidths), start=1):
    cell = a.cell(row=4, column=i, value=c); cell.font = H2; cell.fill = DARK; cell.alignment = Alignment(wrap_text=True, vertical="center")
    a.column_dimensions[get_column_letter(i)].width = w
a.row_dimensions[4].height = 32
arows = [
    ["Історична норма", 200, 200, 45, None, None, "25–65 переписок за $130–320/міс, $2,92–6,86 за переписку (target-osnovy.md)"],
    ["Вересень 2026", None, None, None, None, None, ""],
    ["Жовтень 2026", None, None, None, None, None, ""],
    ["Листопад 2026", None, None, None, None, None, ""],
    ["Грудень 2026", None, None, None, None, None, ""],
]
for r, row in enumerate(arows, start=5):
    for c, v in enumerate(row[:6], start=1):
        cell = a.cell(row=r, column=c, value=v); cell.font = BLUE; cell.border = BOX
        if c in (2,3): cell.number_format = USD
        if c in (4,5,6): cell.number_format = NUM
        if c > 1: cell.fill = YELLOW
    a.cell(row=r, column=10, value=row[6]).font = GREY
    for c, f in ((7, f"=IF(D{r}=0,0,C{r}/D{r})"), (8, f"=IF(E{r}=0,0,C{r}/E{r})"), (9, f"=IF(F{r}=0,0,C{r}/F{r})")):
        cell = a.cell(row=r, column=c, value=f); cell.font = BLACK; cell.number_format = USD; cell.border = BOX
pr = 5 + len(arows) + 1
a.cell(row=pr, column=1, value="ПЛАН (з аркуша Вхідні)").font = BOLD
for c, f, fmt in ((2, "=Вхідні!B26", USD), (3, "=Вхідні!B26", USD), (4, "=Вхідні!B27", NUM), (5, "=Вхідні!B27*Вхідні!B28", NUM), (6, "=Вхідні!B27*Вхідні!B28*Вхідні!B29", NUM)):
    cell = a.cell(row=pr, column=c, value=f); cell.font = GREEN; cell.number_format = fmt
for c, f in ((7, f"=IF(D{pr}=0,0,C{pr}/D{pr})"), (8, f"=IF(E{pr}=0,0,C{pr}/E{pr})"), (9, f"=IF(F{pr}=0,0,C{pr}/F{pr})")):
    cell = a.cell(row=pr, column=c, value=f); cell.font = BOLD; cell.number_format = USD
lr = pr + 2
a.cell(row=lr, column=1, value="ЧИ ОКУПАЄТЬСЯ РЕКЛАМА").font = H2; a.cell(row=lr, column=1).fill = DARK
a.cell(row=lr+1, column=1, value="Вартість клієнта, грн").font = BLACK
c = a.cell(row=lr+1, column=2, value=f"=I{pr}*Вхідні!B25"); c.number_format = UAH; c.font = BLACK
a.cell(row=lr+2, column=1, value="Клієнт приносить за весь час, грн (ціна × місяців)").font = BLACK
c = a.cell(row=lr+2, column=2, value="=Вхідні!B4*Вхідні!B30"); c.number_format = UAH; c.font = GREEN
a.cell(row=lr+3, column=1, value="Валова маржа за весь час, грн").font = BLACK
c = a.cell(row=lr+3, column=2, value="=Юніт!B9*Вхідні!B30"); c.number_format = UAH; c.font = GREEN
a.cell(row=lr+4, column=1, value="Маржа / вартість клієнта").font = BOLD
c = a.cell(row=lr+4, column=2, value=f"=IF(B{lr+1}=0,0,B{lr+3}/B{lr+1})"); c.number_format = '0.0"x"'; c.font = BOLD
a.cell(row=lr+4, column=3, value="Норма для агенцій — від 3x. Менше — реклама з'їдає клієнта").font = GREY

# ---------------- Команда ----------------
t = wb.create_sheet("Команда")
tcols = ["Роль", "Формат", "Ставка", "За що", "Обсяг на місяць (ціль, 10 клієнтів)", "Вартість на місяць", "Статус", "Коментар"]
twidths = [30, 12, 14, 12, 22, 18, 16, 46]
t["A1"] = "КОМАНДА — хто що робить і скільки коштує"; t["A1"].font = H1
t["A2"] = "Обсяг рахується для сценарію «Ціль». Ставки тягнуться з аркуша Вхідні"; t["A2"].font = GREY
for i, (c, w) in enumerate(zip(tcols, twidths), start=1):
    cell = t.cell(row=4, column=i, value=c); cell.font = H2; cell.fill = DARK; cell.alignment = Alignment(wrap_text=True, vertical="center")
    t.column_dimensions[get_column_letter(i)].width = w
t.row_dimensions[4].height = 32
trows = [
    ["Оксана — власник", "—", None, "—", None, None, "є", "Продажі, стратегія, ціни, контроль. Не зйомка"],
    ["Оператор", "підряд", "=Вхідні!B10", "ролик", "=Вхідні!B8*Вхідні!B39", "=C6*E6", "є / знайти", "Поки Оксана знімає сама — ця витрата = 0, але її час = Вхідні!B15"],
    ["Монтажер", "підряд", "=Вхідні!B11", "ролик", "=Вхідні!B8*Вхідні!B39", "=C7*E7", "є / знайти", ""],
    ["Валерія — каруселі й дизайн", "підряд", "=Вхідні!B12", "карусель", "=Вхідні!B6*Вхідні!B39", "=C8*E8", "є", ""],
    ["Режисер-менеджер зйомок", "штат", "=Вхідні!B21", "місяць", 1, "=C9*E9", "НАЙНЯТИ ПЕРШИМ", "Знімає Оксану з майданчика. Ostrovskyi Team: 30–40 тис., Київ"],
    ["Project manager", "штат", "=Вхідні!B22", "місяць", 1, "=C10*E10", "від 6 клієнтів", "Веде клієнтів: дедлайни, узгодження, оплати. Ostrovskyi Team: 45–60 тис."],
    ["Таргетолог", "підряд", 8000, "місяць", 1, "=C11*E11", "опційно", "ПРИПУЩЕННЯ по ставці. Або регламент + Оксана раз на тиждень"],
    ["Агент (я)", "—", 0, "—", None, 0, "є", "Конкуренти, референси, сценарії-чернетки, тексти, КП, таблиці, календар, звіти по таргету"],
]
for r, row in enumerate(trows, start=5):
    for c, v in enumerate(row, start=1):
        cell = t.cell(row=r, column=c, value=v); cell.border = BOX
        cell.font = GREEN if isinstance(v, str) and v.startswith("=Вхідні") else (BLACK if isinstance(v, str) and v.startswith("=") else BLUE)
        if c in (3, 6): cell.number_format = UAH
        if c == 5: cell.number_format = NUM
        if c == 8: cell.font = GREY
t.cell(row=11, column=3).fill = YELLOW
tt = 5 + len(trows) + 1
t.cell(row=tt, column=1, value="РАЗОМ на місяць при 10 клієнтах").font = BOLD
c = t.cell(row=tt, column=6, value=f"=SUM(F5:F{tt-2})"); c.font = BOLD; c.number_format = UAH
t.cell(row=tt+1, column=1, value="Дохід при 10 клієнтах за ціною-ціллю").font = BLACK
c = t.cell(row=tt+1, column=6, value="=Місяць!D6"); c.font = GREEN; c.number_format = UAH
t.cell(row=tt+2, column=1, value="Частка команди в доході").font = BOLD
c = t.cell(row=tt+2, column=6, value=f"=IF(F{tt+1}=0,0,F{tt}/F{tt+1})"); c.font = BOLD; c.number_format = PCT
t.cell(row=tt+2, column=8, value="Норма для продакшн-агенцій — 40–55%. Вище 60% — ціна пакета замала").font = GREY

for sh in wb.worksheets:
    sh.sheet_view.showGridLines = False
    sh.freeze_panes = "A5" if sh.title in ("Клієнти", "Реклама", "Команда") else None

out = "/tmp/claude-0/-home-user-jarvis/9b0f16d0-b599-5d4d-bcf6-1376d58736c9/scratchpad/model/finmodel-rils-agency.xlsx"
wb.save(out); print("saved", out)
