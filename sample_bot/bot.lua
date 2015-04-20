-- Simple Telegram Bot

require('utils')
ready = 0

-- Hooks
function on_msg_receive (msg)

  -- are we ready?
  if ready == 0 then
    return
  end

  -- who will receive the response messages
  local receiver = get_receiver(msg)

  if msg_valid(msg) then

    if string_starts(msg.text, '!ping') then

      send_msg(receiver, '(bot) pong '..msg.from.first_name, ok_cb, false)
    end

    -- ping google dns
    if string_starts(msg.text, '!ping google') then

      local handle = io.popen('ping -c 1 8.8.8.8')
      local result = handle:read("*a")
      handle:close()
      send_large_msg(receiver, result)
    end

    -- ping localhost
    if string_starts(msg.text, '!ping localhost') then

      local handle = io.popen('ping6 -c 1 ::1')
      local result = handle:read("*a")
      handle:close()
      send_large_msg(receiver, result)
    end

    -- ping custom host
    if string_starts(msg.text, '!cping') then

      -- extract the shell command to run
      -- by removing the command identifier
      command = msg.text:gsub('!cping', '')
      command = (receiver, 'ping -c 1 '.. shell_escape(command))
      send_large_msg(receiver, 'Running command: '..command)

      -- run the command
      local handle = io.popen(command)
      local result = handle:read("*a")
      handle:close()
      send_large_msg(receiver, result)
    end

  end
end

function on_our_id (id)
end

function on_secret_chat_created (peer)
end

function on_user_update (user)
end

function on_chat_update (user)
end

function on_get_difference_end ()
end

function on_binlog_replay_end ()
  ready = 1
end

