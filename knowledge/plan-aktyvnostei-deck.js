const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10 x 5.625

const BG = '0D0D0D';
const HEAD = 'E8D6B3';
const WHITE = 'FFFFFF';
const CARD = 'F3E9D7';
const DARK = '1A1A1A';
const MUTED = '9A9A9A';
const F = 'Calibri';

function slide() {
  const s = pres.addSlide();
  s.background = { color: BG };
  return s;
}

function title(s, txt) {
  s.addText(txt, {
    x: 0.6, y: 0.35, w: 8.8, h: 0.7, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 32, bold: true, color: HEAD, charSpacing: 1,
    align: 'left', valign: 'middle'
  });
}

function card(s, x, y, w, h) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, fill: { color: CARD }, rectRadius: 0.12, line: { color: CARD }
  });
}

function numCircle(s, x, y, n) {
  s.addShape(pres.ShapeType.ellipse, {
    x, y, w: 0.42, h: 0.42, fill: { color: HEAD }, line: { color: HEAD }
  });
  s.addText(String(n), {
    x, y, w: 0.42, h: 0.42, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 14, bold: true, color: DARK, align: 'center', valign: 'middle'
  });
}

/* ---------- 1. Title ---------- */
{
  const s = slide();
  s.addText('ПЛАН АКТИВНОСТЕЙ', {
    x: 0.6, y: 1.45, w: 8.8, h: 1.0, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 44, bold: true, color: HEAD, charSpacing: 2, valign: 'bottom'
  });
  s.addText('ksysha.bogdanets — креативне агентство', {
    x: 0.6, y: 2.5, w: 8.8, h: 0.35, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 16, color: WHITE
  });
  s.addText('Вересень 2026', {
    x: 0.6, y: 2.88, w: 8.8, h: 0.3, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 12, color: MUTED
  });
  const chips = ['ПРОДАЖІ', 'САЙТИ', 'СТВОРЕННЯ КОНТЕНТУ'];
  chips.forEach((c, i) => {
    const x = 0.6 + i * 3.0;
    card(s, x, 3.9, 2.75, 0.62);
    s.addText(c, {
      x, y: 3.9, w: 2.75, h: 0.62, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 12, bold: true, color: DARK, align: 'center', valign: 'middle', charSpacing: 1
    });
  });
  s.addNotes('Три напрямки роботи: продажі, сайти, створення контенту.');
}

/* ---------- 2. Продажі ---------- */
{
  const s = slide();
  title(s, 'БЛОК 1. ПРОДАЖІ');
  const items = [
    'Обробляти заявки',
    'Виводити людей на зуми',
    'Закривати на угоди',
    'Писати старим клієнтам, нагадувати за зуми'
  ];
  items.forEach((t, i) => {
    const y = 1.35 + i * 0.62;
    numCircle(s, 0.6, y, i + 1);
    s.addText(t, {
      x: 1.2, y, w: 8.2, h: 0.42, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 16, color: WHITE, valign: 'middle'
    });
  });
  card(s, 0.6, 4.05, 8.8, 0.95);
  s.addText('ОКРЕМА ЗАДАЧА', {
    x: 0.95, y: 4.18, w: 8.1, h: 0.28, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 11, bold: true, color: '7A6A4F', charSpacing: 1
  });
  s.addText('Створити презентацію для тих, хто заповнив квіз', {
    x: 0.95, y: 4.48, w: 8.1, h: 0.4, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 17, bold: true, color: DARK
  });
  s.addNotes('Календар: Пн, Ср, Пт 11:30. Презентація — Ср і Пт 12:30.');
}

/* ---------- 3. Сайти ---------- */
{
  const s = slide();
  title(s, 'БЛОК 2. САЙТИ');

  card(s, 0.6, 1.3, 4.2, 1.5);
  s.addText('РІЛС ПІД КЛЮЧ', {
    x: 0.9, y: 1.5, w: 3.6, h: 0.35, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 18, bold: true, color: DARK, charSpacing: 1
  });
  s.addText('Сайт під послугу', {
    x: 0.9, y: 1.92, w: 3.6, h: 0.7, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 14, color: '4A4A4A'
  });

  card(s, 0.6, 3.05, 4.2, 1.7);
  s.addText('НАВЧАННЯ З НУЛЯ', {
    x: 0.9, y: 3.25, w: 3.6, h: 0.35, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 18, bold: true, color: DARK, charSpacing: 1
  });
  s.addText('Для тих, хто стартує в Instagram.\nЦіна нижче ринку', {
    x: 0.9, y: 3.67, w: 3.6, h: 0.85, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 14, color: '4A4A4A'
  });

  s.addText('НАВІЩО ВОНИ', {
    x: 5.3, y: 1.3, w: 4.1, h: 0.35, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 15, bold: true, color: HEAD, charSpacing: 1
  });
  const why = [
    'Йдуть у таргетовану рекламу',
    'Стоять на сторінці в Instagram',
    'Відправляються клієнтам напряму',
    'Під кожен зняті відео'
  ];
  why.forEach((t, i) => {
    const y = 1.85 + i * 0.72;
    s.addShape(pres.ShapeType.ellipse, {
      x: 5.3, y: y + 0.09, w: 0.16, h: 0.16, fill: { color: HEAD }, line: { color: HEAD }
    });
    s.addText(t, {
      x: 5.65, y, w: 3.75, h: 0.5, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 15, color: WHITE, valign: 'top'
    });
  });
  s.addNotes('Календар: Пн, Ср, Пт 10:00.');
}

/* ---------- 4. Контент — наставництво ---------- */
{
  const s = slide();
  title(s, 'БЛОК 3.1. КОНТЕНТ — НАСТАВНИЦТВО');
  s.addText('Ланцюжок від референсу до готового рілс', {
    x: 0.6, y: 1.08, w: 8.8, h: 0.3, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 13, color: MUTED
  });
  const steps = [
    'Аналіз конкурентів',
    'Скрайбінг референсів',
    'Транскрибація',
    'Створення сценаріїв',
    'Запис рілс',
    'Монтаж'
  ];
  steps.forEach((t, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 3.0;
    const y = 1.55 + row * 1.65;
    card(s, x, y, 2.75, 1.4);
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.25, y: y + 0.22, w: 0.4, h: 0.4, fill: { color: '2B2B2B' }, line: { color: '2B2B2B' }
    });
    s.addText(String(i + 1), {
      x: x + 0.25, y: y + 0.22, w: 0.4, h: 0.4, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 13, bold: true, color: HEAD, align: 'center', valign: 'middle'
    });
    s.addText(t, {
      x: x + 0.25, y: y + 0.72, w: 2.3, h: 0.55, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 14, bold: true, color: DARK
    });
  });
  s.addNotes('Календар: Вт, Чт, Сб 10:00 — написання сценаріїв.');
}

/* ---------- 5. Контент — рілс під ключ ---------- */
{
  const s = slide();
  title(s, 'БЛОК 3.2. КОНТЕНТ — РІЛС ПІД КЛЮЧ');
  s.addText('Контент під послугу', {
    x: 0.6, y: 1.08, w: 8.8, h: 0.3, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 13, color: MUTED
  });
  const blocks = [
    ['РУБРИКИ', 'Розробити рубрики.\nНаприклад: «як би я просувала Instagram косметолога»'],
    ['КОНКУРЕНТИ', 'Аналіз конкурентів\nу ніші послуги'],
    ['СЦЕНАРІЇ', 'Створити сценарії\nпід послугу']
  ];
  blocks.forEach((b, i) => {
    const x = 0.6 + i * 3.0;
    card(s, x, 1.6, 2.75, 2.6);
    s.addText(b[0], {
      x: x + 0.28, y: 1.85, w: 2.2, h: 0.35, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 16, bold: true, color: DARK, charSpacing: 1
    });
    s.addText(b[1], {
      x: x + 0.28, y: 2.3, w: 2.2, h: 1.6, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 13, color: '4A4A4A'
    });
  });
  s.addNotes('Календар: Вт, Чт, Сб 10:00 і 12:00.');
}

/* ---------- 6. Тижневий графік ---------- */
{
  const s = slide();
  title(s, 'ТИЖНЕВИЙ ГРАФІК');

  const cols = [
    ['ПН · СР · ПТ', ['Сайт', 'Таргет', 'Продажі', 'Кейс на сторінку', 'Шаблон презентації', 'Клієнти', 'Звільнимо (ТГ)']],
    ['ВТ · ЧТ · СБ', ['Написання сценаріїв', 'Instagram агенції', 'Відгуки', 'Чистка папок', 'Каруселі та відео', 'Клієнти', 'Ефіри та розбори']]
  ];
  cols.forEach((c, i) => {
    const x = 0.6 + i * 4.6;
    card(s, x, 1.2, 4.2, 3.2);
    s.addText(c[0], {
      x: x + 0.3, y: 1.42, w: 3.6, h: 0.35, isTextBox: true, margin: 0,
      fontFace: F, fontSize: 17, bold: true, color: DARK, charSpacing: 1
    });
    c[1].forEach((t, j) => {
      s.addText(t, {
        x: x + 0.3, y: 1.9 + j * 0.33, w: 3.6, h: 0.3, isTextBox: true, margin: 0,
        fontFace: F, fontSize: 13, color: '3A3A3A'
      });
    });
  });
  s.addText('Неділя вільна   ·   старт щодня о 10:00', {
    x: 0.6, y: 4.65, w: 8.8, h: 0.4, isTextBox: true, margin: 0,
    fontFace: F, fontSize: 14, bold: true, color: HEAD, align: 'center', charSpacing: 1
  });
  s.addNotes('Червоним у календарі позначені важливі задачі.');
}

pres.writeFile({ fileName: '/tmp/claude-0/-home-user-jarvis/9b0f16d0-b599-5d4d-bcf6-1376d58736c9/scratchpad/deck/plan-aktyvnostei.pptx' })
  .then(f => console.log('OK', f));
