local Types = require(script.Parent.Types)

local function Buffer(str, allowOverflows): Types.Buffer
    local Stream = {}
    Stream.Offset = 0
    Stream.Source = str
    Stream.Length = string.len(str)
    Stream.IsFinished = false
    Stream.LastUnreadBytes = 0
    Stream.AllowOverflows = allowOverflows or true

    function Stream.read(self, len, shift)
        local len = len or 1
        local shift = shift or true
        local dat = string.sub(self.Source, self.Offset + 1, self.Offset + len)

        local dataLength = string.len(dat)
        local unreadBytes = len - dataLength

        if unreadBytes > 0 and not self.AllowOverflows then
            error("Buffer went out of bounds and AllowOverflows is false")
        end

        if shift then
            self:seek(len)
        end

        self.LastUnreadBytes = unreadBytes
        return dat
    end

    function Stream.seek(self, len)
        local len = len or 1

        self.Offset = math.clamp(self.Offset + len, 0, self.Length)
        self.IsFinished = self.Offset >= self.Length
    end

    function Stream.append(self, newData)
        -- adds new data to the end of a stream
        self.Source = self.Source .. newData
        self.Length = string.len(self.Source)
        self:seek(0) --hacky but forces a recalculation of the isFinished flag
    end

    function Stream.toEnd(self)
        self:seek(self.Length)
    end

    function Stream.readNumber(self, fmt, shift)
        fmt = fmt or "I1"
        local packsize = string.packsize(fmt)

        local chunk = self:read(packsize, shift)
        local n = string.unpack(fmt, chunk)
        return n
    end

    return Stream
end

return Buffer
