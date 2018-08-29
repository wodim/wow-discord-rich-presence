frame_count = 0
frames = {}
last_status = nil

function IPC_CreateFrames()
    local size = 12

    frame_count = math.floor(GetScreenWidth() / size)
    -- print("Max bytes that can be stored: " .. (frame_count * 3) - 1)

    for i=1, frame_count do
        frames[i] = CreateFrame("Frame", nil, UIParent)
        frames[i]:SetFrameStrata("TOOLTIP")
        frames[i]:SetWidth(size)
        frames[i]:SetHeight(size)

        -- initialise it as black
        local t = frames[i]:CreateTexture(nil, "TOOLTIP")
        t:SetTexture(0, 0, 0, 0)
        t:SetAllPoints(frames[i])
        frames[i].texture = t

        frames[i]:SetPoint("TOPLEFT", (i - 1) * size, 0)
        frames[i]:Show()
    end

    return frames
end

function IPC_PaintFrame(frame, r, g, b, force)
    -- turn them into black if they are null
    if r == nil then r = 0 end
    if g == nil then g = 0 end
    if b == nil then b = 0 end

    -- from 0-255 to 0.0-1.0
    r = r / 255
    g = g / 255
    b = b / 255

    -- set alpha to 1 if this pixel is black and force is 0 or null
    if r == 0 and g == 0 and b == 0 and (force == 0 or force == nil) then a = 0 else a = 1 end

    -- and now paint it
    frame.texture:SetTexture(r, g, b, a)
    frame.texture:SetAllPoints(frame)
end

function IPC_CleanFrames()
    for i=1, frame_count do
        IPC_PaintFrame(frames[i], 0, 0, 0, 0)
    end
end

function IPC_PaintSomething(text)
    local max_bytes = (frame_count - 1) * 3
    if string.len(text) >= max_bytes then
        -- print("You're painting too many bytes (" .. string.len(text) .. " vs " .. max_bytes .. ")")
        return
    end

    -- clean all
    IPC_CleanFrames()

    local black_square_idx = 1

    for squares_painted=1, math.ceil(string.len(text) / 3) do
        local offset = (squares_painted - 1) * 3 + 1
        local trio = string.sub(text, offset, offset + 2)
        r = 0; g = 0; b = 0
        r = string.byte(string.sub(trio, 1,1))
        if string.len(trio) > 1 then g = string.byte(string.sub(trio, 2, 2)) end
        if string.len(trio) > 2 then b = string.byte(string.sub(trio, 3, 3)) end
        IPC_PaintFrame(frames[squares_painted], r, g, b)
        black_square_idx = squares_painted + 1
    end

    -- and then paint the last one black
    IPC_PaintFrame(frames[black_square_idx], 0, 0, 0, 1)
end

function GetContinentName(continentID)
    -- this is here because it doesn't exist in wotlk. if you are porting this
    -- to retail you'll just have to remove this whole function.
    if continentID == 1 then
        return 'Kalimdor'
    elseif continentID == 2 then
        return 'Eastern Kingdoms'
    elseif continentID == 3 then
        return 'Outland'
    elseif continentID == 4 then
        return 'Northrend'
    end
end

function IPC_EncodeZoneType()
    local zone_name = GetRealZoneText()
    -- if the world map is open we can't rely on it so send the last status
    -- or something generic if we've never seen a status
    if WorldMapFrame:IsVisible() then
        if last_status == nil then
            status = 'In the overworld'
        else
            status = last_status
        end
    else
        local continent_name = GetContinentName(GetCurrentMapContinent())
        if continent_name then
            status = continent_name
            last_status = status
        else
            status = 'In the overworld'
        end
    end
    if zone_name == "" or zone_name == nil then return nil end
    local encoded = "|" .. zone_name .. "|" .. status .. "|"
    return encoded
end

-- received addon events.
function IPC_OnEvent(this, event, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10)
    if event == "PLAYER_LOGIN" then
        IPC_CreateFrames()
    elseif event == "PLAYER_ENTERING_WORLD" or event == "ZONE_CHANGED_NEW_AREA" or event == "WORLD_MAP_UPDATE" then
        local encoded = IPC_EncodeZoneType()
        if encoded ~= nil then IPC_PaintSomething(encoded) end
    end
end

function IPC_OnLoad()
    IPCFrame:RegisterEvent("PLAYER_LOGIN")
    IPCFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
    IPCFrame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
    IPCFrame:RegisterEvent("WORLD_MAP_UPDATE")
    SlashCmdList["IPC"] = IPC_PaintSomething
    SLASH_IPC1 = "/ipc"
    SlashCmdList["CLEAN"] = IPC_CleanFrames
    SLASH_CLEAN1 = "/clean"
end

function print(text) DEFAULT_CHAT_FRAME:AddMessage(text) end
