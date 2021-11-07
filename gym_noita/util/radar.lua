local cx, cy = GameGetCameraPos()
local enemies = nil
for i, v in ipairs(EntityGetInRadiusWithTag(cx, cy, 500, "enemy") or {}) do
  local x, y = EntityGetTransform(v)
  print(x, ' ', y)
end
