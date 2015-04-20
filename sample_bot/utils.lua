-- Some Init Vars
now = os.time()

-- Utils

-- get_receiver
--  Determine who should get a response
--  message.
function get_receiver(msg)
  if msg.to.type == 'user' then
    return 'user#id'..msg.from.id
  end
  if msg.to.type == 'chat' then
    return 'chat#id'..msg.to.id
  end
  if msg.to.type == 'encr_chat' then
    return msg.to.print_name
  end
end

-- msg_valid
--  Determines if a message is valid based
--  on time and read status.
function msg_valid(msg)
  -- Dont process outgoing messages
--  if msg.out then
--    print("Not valid, msg from us")
--    return false
--  end

  -- Before bot was started
  if msg.date < now then
    print("Not valid, old msg")
    return false
  end

  if msg.unread == 0 then
    print("Not valid, readed")
    return false
  end

  return true
end

-- vardump
--  Dumps the contents of a variable
function vardump(value, depth, key)
  local linePrefix = ''
  local spaces = ''

  if key ~= nil then
    linePrefix = '[' .. key .. '] = '
  end

  if depth == nil then
    depth = 0
  else
    depth = depth + 1
    for i=1, depth do spaces = spaces .. '  ' end
  end

  if type(value) == 'table' then
    mTable = getmetatable(value)
    if mTable == nil then
      print(spaces ..linePrefix..'(table) ')
    else
      print(spaces ..'(metatable) ')
        value = mTable
    end
    for tableKey, tableValue in pairs(value) do
      vardump(tableValue, depth, tableKey)
    end
  elseif type(value)	== 'function' or
      type(value)	== 'thread' or
      type(value)	== 'userdata' or
      value		== nil
  then
    print(spaces..tostring(value))
  else
    print(spaces..linePrefix..'('..type(value)..') '..tostring(value))
  end
end

-- send_large_msg
--  Wraps send_large_msg_callback so that it may
--  have friendlier parameters
function send_large_msg(destination, text)
  local cb_extra = {
    destination = destination,
    text = text
  }
  send_large_msg_callback(cb_extra, true)
end

-- send_large_msg_callback
--  If text is longer than 4096 chars, send multiple msg.
--  https://core.telegram.org/method/messages.sendMessage
function send_large_msg_callback(cb_extra, success, result)
  local text_max = 4096

  local destination = cb_extra.destination
  local text = cb_extra.text
  local text_len = string.len(text)
  local num_msg = math.ceil(text_len / text_max)

  if num_msg <= 1 then
    send_msg(destination, text, ok_cb, false)
  else

    local my_text = string.sub(text, 1, 4096)
    local rest = string.sub(text, 4096, text_len)

    local cb_extra = {
      destination = destination,
      text = rest
    }

    send_msg(destination, my_text, send_large_msg_callback, cb_extra)
  end
end

-- shell_escape
--  Remove obviously bad characters in an
--  attempt to sanitize shell commands
function shell_escape(...)
  local s = ...
  local out = ''

  for c in s:gmatch'.' do
    if not c:find '[^A-Za-z0-9_./-]' then
     out = out .. c
    end
  end

  return out
end

-- string_starts
--  Determine if a string starts with start
function string_starts(string, start)
   return string.sub(string, 1, string.len(start)) == start
end
