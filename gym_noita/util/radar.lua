local cx, cy = GameGetCameraPos()
local output = '{ '

local bool_to_int = { [true]=1, [false]=0 }

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

    local has_shot = tostring(bool_to_int[not did_hit])

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
  
  local range = 50

  local n_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x, p_y - range)
  local ne_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x + range, p_y - range)
  local e_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x + range, p_y)  
  local se_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x + range, p_y + range)
  local s_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x, p_y + range)
  local sw_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x - range, p_y + range)
  local w_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x - range, p_y)
  local nw_blocked_v, x, y = RaytracePlatforms(p_x, p_y, p_x - range, p_y - range)
  
  
  local n_blocked = '"north_blocked": ' .. tostring(bool_to_int[n_blocked_v]) .. ', '
  local ne_blocked = '"northeast_blocked": ' .. tostring(bool_to_int[ne_blocked_v]) .. ', '
  local e_blocked = '"east_blocked": ' .. tostring(bool_to_int[e_blocked_v]) .. ', '
  local se_blocked = '"southeast_blocked": ' .. tostring(bool_to_int[se_blocked_v]) .. ', '
  local s_blocked = '"south_blocked": ' .. tostring(bool_to_int[s_blocked_v]) .. ', '
  local sw_blocked = '"southwest_blocked": ' .. tostring(bool_to_int[sw_blocked_v]) .. ', '
  local w_blocked = '"west_blocked": ' .. tostring(bool_to_int[w_blocked_v]) .. ', '
  local nw_blocked = '"northwest_blocked": ' .. tostring(bool_to_int[nw_blocked_v]) .. ', '
  -- collect output
  output = output .. pos
  output = output .. hp
  output = output .. max_hp
  output = output .. money
  output = output .. n_blocked
  output = output .. ne_blocked
  output = output .. e_blocked
  output = output .. se_blocked
  output = output .. s_blocked
  output = output .. sw_blocked
  output = output .. w_blocked
  output = output .. nw_blocked
  output = output .. enemies
else
  output = output .. ' "state": "player is dead"'
end
-- close output
output = output .. ' }'
print(output)
