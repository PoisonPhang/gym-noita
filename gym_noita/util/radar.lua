local cx, cy = GameGetCameraPos()
local output = '{ '

-- loop through enemy positions and build array
enemies =  '"enemies": [ '
for i, v in ipairs(EntityGetInRadiusWithTag(cx, cy, 250, 'enemy') or {}) do
  local name = EntityGetName(v)
  local x, y = EntityGetTransform(v)
  local enemy = ' { "name": ' .. '"' .. tostring(name) .. '"' .. ', "x": ' .. tostring(x) .. ', "y": ' .. tostring(y) .. ' },'
  enemies = enemies .. enemy
end
enemies = string.sub(enemies, 1, -2)
enemies = enemies .. ' ]'

local wallet = EntityGetComponent(get_player(), 'WalletComponent')[1]
local dmg_comp = EntityGetComponent(get_player(), 'DamageModelComponent')[1]

hp_v = ComponentGetValue2(dmg_comp, 'hp')
max_hp_v = ComponentGetValue2(dmg_comp, 'max_hp')
money_v = ComponentGetValue2(wallet, 'money')

local p_x, p_y = EntityGetTransform(get_player()) 
local pos = '"pos": { "x": ' .. tostring(p_x) .. ', "y": ' .. tostring(p_y) .. ' }, '
local hp = '"hp": ' .. tostring(hp_v) .. ', '
local max_hp = '"max_hp": ' .. tostring(max_hp_v) .. ', '
local money = '"money": ' .. tostring(money_v) .. ', '

-- collect output
output = output .. pos
output = output .. hp
output = output .. max_hp
output = output .. money
output = output .. enemies
-- close output
output = output .. ' }'
print(output)
