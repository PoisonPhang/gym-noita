local cx, cy = GameGetCameraPos()
local output = '{ '

local wallets = EntityGetComponent(get_player(), 'WalletComponent')
local dmg_comps = EntityGetComponent(get_player(), 'DamageModelComponent')

if (not (wallets == nil and dmg_comps == nil))
then
  local wallet = wallets[1]
  local dmg_comp = dmg_comps[1]
  local p_x, p_y = EntityGetTransform(get_player())
  
  -- loop through enemy positions and build array
  enemies =  '"enemies": [ '
  for i, v in ipairs(EntityGetInRadiusWithTag(cx, cy, 250, 'enemy') or {}) do
    local name = EntityGetName(v)
    local x, y = EntityGetTransform(v)
    local did_hit, hit_x, hit_y = RaytracePlatforms(p_x, p_y, x, y)

    local has_shot = ""

    if (did_hit)
    then
      has_shot = 'false'
    else
      has_shot = 'true'
    end

    local enemy = ' { "name": ' .. '"' .. tostring(name) .. '"' .. ', "x": ' .. tostring(x) .. ', "y": ' .. tostring(y) .. ', "has_shot":' .. has_shot .. ' },'
    enemies = enemies .. enemy
  end
  enemies = string.sub(enemies, 1, -2)
  enemies = enemies .. ' ]'
  
  hp_v = ComponentGetValue2(dmg_comp, 'hp')
  max_hp_v = ComponentGetValue2(dmg_comp, 'max_hp')
  money_v = ComponentGetValue2(wallet, 'money')
   
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
else
  output = output .. ' "state": "player is dead"'
end
-- close output
output = output .. ' }'
print(output)
