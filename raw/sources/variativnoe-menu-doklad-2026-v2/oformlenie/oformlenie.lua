-- Layout-only filter: wraps existing text in styled containers; changes no wording.
local fmt = FORMAT
local function lead(blk)
  if blk.t ~= "Para" then return nil end
  local f = blk.content[1]
  if f and f.t == "Strong" then return pandoc.utils.stringify(f) end
end
local function box(cls, style, blocks, title)
  local inner = {}
  if title then
    table.insert(inner, pandoc.Div({pandoc.Para({pandoc.Str(title)})}, pandoc.Attr("", {"box-label"}, {["custom-style"]="Box Label"})))
  end
  for _, b in ipairs(blocks) do table.insert(inner, b) end
  return pandoc.Div(inner, pandoc.Attr("", {"callout", cls}, {["custom-style"]=style}))
end
local BADGE = {["Норма"]="norma", ["Толкование"]="tolk", ["Рекомендация"]="rek", ["Локальная форма"]="lok"}

function Table(t)
  local hdr = pandoc.utils.stringify(t.head)
  if hdr:match("^Класс") then
    t.attr.classes:insert("classes-table")
    t = t:walk({Strong = function(s)
      local k = BADGE[pandoc.utils.stringify(s)]
      if k then return pandoc.Span({s}, pandoc.Attr("", {"badge", "b-"..k})) end
    end})
  end
  -- plain cells whose whole text is a claim class get a colour badge
  t = t:walk({Plain = function(p)
    local k = BADGE[pandoc.utils.stringify(p)]
    if k and #p.content <= 3 then return pandoc.Plain({pandoc.Span(p.content, pandoc.Attr("", {"badge", "b-"..k}))}) end
  end})
  return t
end

function Pandoc(doc)
  local blocks = doc.blocks
  -- exec summary from the bold lead sentences of the numbered conclusions in «Заключение»
  local leads, inzak = {}, false
  for _, b in ipairs(blocks) do
    if b.t == "Header" and b.level == 1 then inzak = pandoc.utils.stringify(b):match("^Заключение") ~= nil end
    if inzak and b.t == "OrderedList" and #leads == 0 then
      for _, item in ipairs(b.content) do
        local p = item[1]
        if p and (p.t == "Para" or p.t == "Plain") and p.content[1] and p.content[1].t == "Strong" then
          table.insert(leads, {pandoc.Plain(p.content[1].content)})
        end
      end
    end
  end
  local out, i = {}, 1
  while i <= #blocks do
    local b = blocks[i]
    if b.t == "Header" and b.level == 1 and pandoc.utils.stringify(b) == "Сведения о документе" and #leads > 0 then
      table.insert(out, box("exec-summary", "Box Summary", {
        pandoc.OrderedList(leads),
        pandoc.Para({pandoc.Emph({pandoc.Str("Краткое изложение составлено из выделенных положений Заключения; полные формулировки, оговорки и ссылки на источники — в Заключении и выводах по главам.")})})
      }, "Основные выводы доклада"))
    end
    if b.t == "Header" and b.level == 2 and pandoc.utils.stringify(b):match("^Выводы по главе") then
      local grp = {}
      local j = i + 1
      while j <= #blocks and not (blocks[j].t == "Header" and blocks[j].level <= 2) do
        table.insert(grp, blocks[j]); j = j + 1
      end
      table.insert(out, b)
      table.insert(out, box("conclusions", "Box Conclusion", grp))
      i = j
    else
      local l = lead(b)
      if l and l:match("^Открытый вопрос") then
        table.insert(out, box("open-question", "Box Question", {b}, "Открытый вопрос"))
      elseif l and l:lower():match("открытый вопрос") then
        table.insert(out, box("open-question", "Box Question", {b}, "Открытый вопрос"))
      elseif l == "Классы." then
        table.insert(out, box("claim-classes", "Box Classes", {b}))
      elseif l and (l:match("^Чего доклад не утверждает") or l:match("^Ограничения") or l:match("^Чего источник") or l:match("^Чего источники") or l:match("^Чего делать нельзя") or l:match("^Чего не говорить")) then
        table.insert(out, box("caveat", "Box Caveat", {b}))
      else
        table.insert(out, b)
      end
      i = i + 1
    end
  end
  doc.blocks = out
  return doc
end
