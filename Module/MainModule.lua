local InsertCloud = {}

_Settings = {
    -- SETTINGS FOR INSERT CLOUD

    SandboxScripts = true, -- Sandboxes the scripts, which can protect your game from malicious scripts.
    -- If you are inserting only your own models, then you should disable this.
    DisableScripts = true, -- Disables scripts on load. This is to prevent scripts running
    -- the moment it is loaded.
    CompileAssetAfterLoad = false, -- Compiles asset after being loaded.
    UnlockParts = true, -- Unlocks BaseParts in the model. If disabled, it will allow parts to be locked.
    DefaultParent = workspace, -- The default parent for LoadAsset
    DefaultCompileParent = workspace, -- The default parent for CompileAsset
    DefaultSettings = {}, -- The default settings for LoadAsset.
    DefaultPos = Vector3.new(0, 0, 0) -- The default position for the loaded asset to move to.
}
HTTPS = game:GetService("HttpService")
Replicated = game:GetService("ReplicatedStorage")
MarketPlaceService = game:GetService("MarketplaceService")
InsertService = game:GetService("InsertService")
Sandbox = require(script:FindFirstChild("CloudBox") or Replicated:FindFirstChild("CloudBox"))
LocalLoad = require(script:FindFirstChild("Loadstring") or Replicated:FindFirstChild("Loadstring"))
Templates = script:FindFirstChild("Templates") or Replicated:FindFirstChild("Templates")
SandboxType = "Normal"
-- Settings were configured to support my Insert Wars game. Feel free to clone this module and change up the settings.

if _Settings.SandboxScripts then
    SandboxType = "Sandbox"
end
-------------

--INIT
pcall(function()
    if Replicated:FindFirstChild("CloudBox") == nil then
        local c = script.CloudBox:Clone()
        c.Parent = Replicated
    end
    if Replicated:FindFirstChild("Loadstring") == nil then
        local l = script.Loadstring:Clone()
        l.Parent = Replicated
    end
    if Replicated:FindFirstChild("Templates") == nil then
        local t = script.Templates:Clone()
        t.Parent = Replicated
    end
end)

if not Replicated:FindFirstChild("GetLink") then
    local GetLink = Instance.new("RemoteFunction", Replicated)
    GetLink.Name = "GetLink"
    GetLink.OnServerInvoke = function(Link)
        local request = HTTPS:RequestAsync({
            Url=Link,
            Method='GET',
            Headers={},
        })
        if request.StatusCode==200 then
            return request.Body
        else
            warn('HTTP ERROR: '..request.Status..'('..request.StatusCode..')')
            return nil
        end
    end
end

ServerCache = Replicated:FindFirstChild("Cache") or Instance.new("Folder", Replicated)
ServerCache.Name = "Cache"

function ColorFunc(Val, Type)
    if Type == "Float" then -- roblox, you're weird
        local Color = BrickColor.new(Val)
        return Color
    end
    if Val.r <= 1 and Val.g <= 1 and Val.b <= 1 then
        local Color = Color3.new(Val.r, Val.g, Val.b)
        return Color
    else
        local Color = Color3.new(Val.r / 255, Val.g / 255, Val.b / 255)
        return Color
    end
end

ValueTypes = {
    ["CFrame"] = function(Val, Type)
        local Pos = Val.Position
        local Rot = Val.LookVector
        local CF = CFrame.new(Pos,Rot)
        return CF
    end,
    ["Vector2"] = function(Val, Type)
        local Vect = Vector2.new(Val.X, Val.Y)
        return Vect
    end,
    ["Vector3"] = function(Val, Type)
        local Vect = Vector3.new(Val.X, Val.Y, Val.Z)
        return Vect
    end,
    ["BrickColor"] = function(Val, Type)
        local Color = BrickColor.new(Val)
        return Color
    end,
    ["Color"] = ColorFunc, --screw rbxm format changes E
    ["Color3"] = ColorFunc,
    ["Color3uint8"] = ColorFunc,
    ["UDim"] = function(Val, Type)
        local UD = UDim.new(Val.Scale, Val.Offset)
        return UD
    end,
    ["UDim2"] = function(Val, Type)
        local UD = UDim2.new(Val.X.Scale, Val.X.Scale, Val.Y.Scale, Val.Y.Offset)
        return UD
    end,
    ["ColorSequence"] = function(Val, Type)
        local Sequences = {}
        for _, v in ipairs(Val) do
            local Key = ColorSequenceKeypoint.new(v.Time, ColorFunc(v.Value, "Color3"), v.Envelope)
            table.insert(Sequences, Key)
        end
        local ColSeq = ColorSequence.new(Sequences)
        return ColSeq
    end,
    ["NumberSequence"] = function(Val, Type)
        local Sequences = {}
        for _, v in ipairs(Val) do
            local Key = NumberSequenceKeypoint.new(v.Time, v.Value, v.Envelope)
            table.insert(Sequences, Key)
        end
        local NumSeq = NumberSequence.new(Sequences)
        return NumSeq
    end,
    ["NumberRange"] = function(Val, Type)
        local Range = NumberRange.new(Val.Min, Val.Max)
        return Range
    end,
    ["Axes"] = function(Val, Type)
        local Ax = Axes.new(not Val.X or Enum.Axis.X, not Val.Y or Enum.Axis.Y, not Val.Z or Enum.Axis.Z)
        return Ax
    end,
    ["PhysicalProperties"] = function(Val, Type)
        local number = Val
        if number.custom_physics == false then
            return nil
        end
        local Physical = PhysicalProperties.new(
            number.density or 1,
            number.friction or 1,
            number.elasticity or 1,
            number.friction_weight or 1,
            number.elasticity_weight or 1
        )
        return Physical
    end,
    ["Ref"] = function(Val, Type, Refs)
        return Refs[Val]
    end
}

local ClassTypes = {
    ["Script"] = function(ClName, ParentObj, Inst, Properties)
        local Object = Templates:FindFirstChild(SandboxType .. ClName):Clone()
        Object.Parent = ParentObj
        return Object
    end,
    ["LocalScript"] = function(ClName, ParentObj, Inst, Properties)
        local Object = Templates:FindFirstChild(SandboxType .. ClName):Clone()
        Object.Parent = ParentObj
        return Object
    end,
    ["ModuleScript"] = function(ClName, ParentObj, Inst, Properties)
        local Object = Templates:FindFirstChild(SandboxType .. ClName):Clone()
        Object.Parent = ParentObj
        return Object
    end,
    ["MeshPart"] = function(ClName, ParentObj, Inst, Properties)
        local Object = Instance.new("Part")
        Object.Parent = ParentObj
        local OrigSize = CompileValue("Size", Inst.Properties.Size)
        local InitSize = CompileValue("MeshSize", Inst.Properties.MeshSize)
        local MeshID = CompileValue("MeshId", Inst.Properties.MeshID)
        local TextID = CompileValue("TextureId", Inst.Properties.TextureID)
        local Mesh = Instance.new("SpecialMesh")
        Mesh.Parent = Object
        Mesh.MeshType = Enum.MeshType.FileMesh
        Mesh.MeshId = MeshID or ""
        Mesh.TextureId = TextID or ""
        Mesh.Scale = OrigSize / InitSize
        return Object
    end,
    ["Humanoid"] = function(ClName, ParentObj, Inst, Properties)
        local Object = Instance.new("Humanoid")
        Object.Parent = ParentObj
        Object.MaxHealth = Properties["MaxHealth"] or 100
        Object.Health =
            pcall(
            function()
                return Properties["Health"]
            end
        ) or Object.MaxHealth
        return Object
    end,
    ["UnionOperation"] = function(ClName, ParentObj, Inst, Properties)
        --union loader.
    end,
}
local PropExceptions = {
    Attachment0 = true,
    Attachment1 = true,
    Part0 = true,
    Part1 = true,
    Value = true,
    Adornee = true,
    NextSelectionUp = true,
    NextSelectionDown = true,
    NextSelectionLeft = true,
    NextSelectionRight = true,
    SelectionImageObject = true,
    PrimaryPart = true,
    SoundGroup = true,
    CameraSubject = true,
    CustomPhysicalProperties = true
}
--------

function CompileValue(Prop, Value, Refs)
    local Val = Value
    local Type = typeof(Value)
    local Func = ValueTypes[Type] or ValueTypes[Prop]
    if Func then
        local New = Func(Val, Type, Refs)
        return New
    else
        if Value ~= nil then
            return Value
        else
            return nil
        end
    end
end

function LoadModel(Base, ParentObj, Model, Refs)
    Refs = Refs or {}
    local Objects = {}
    local function Recursive(Base, ParentObj, Model)
        for i, Inst in ipairs(Model) do
            local ClName = Inst.class_name
            pcall(
                function()
                    if ClName ~= "Message" and ClName ~= "Hint" then
                        local Object
                        local ClassF = ClassTypes[ClName]
                        if ClassF then
                            Object = ClassF(ClName, ParentObj, Inst, Inst.Properties)
                        else
                            Object = Instance.new(ClName)
                            Object.Parent = ParentObj
                        end
                        if Object:IsA("BasePart") then
                            Object.Anchored = true
                            Object.CanCollide = false
                        end
                        Refs[Inst.reference] = Object
                        Objects[Object] = Inst
                        Recursive(Base, Object, Inst.Children)
                    end
                end
            )
        end
    end
    Recursive(Base, ParentObj, Model)
    LoadProps(Objects, Refs)
end

function LoadProps(Objects, Refs)
    for Object, Inst in pairs(Objects) do
        for x, Property in pairs(Inst.Properties) do
            local function iter()
                x = string.sub(x, 0, 1) .. string.sub(x, 2)
                if x == "Color3uint8" then
                    x = "Color"
                elseif x == "Source" then
                    Object.LOAD.Value = Property
                elseif x == "Disabled" and Property == false then
                    Object.IsDisabled.Value = false
                    if _Settings.DisableScripts == false then
                        Object.Disabled = Property
                    end
                elseif x == "Locked" and _Settings.UnlockParts == true then
                    Object.Locked = false
                end
                if (Object[x] ~= nil or PropExceptions[x]) and x ~= "Disabled" and x ~= "Locked" then
                    local CompdVal = CompileValue(x, Property, Refs)
                    Object[x] = CompdVal
                end
            end
            pcall(iter)
        end
    end
end

function InitModel(Model, Parent, Pos, Settings)
    Model.Parent = workspace
    Model:MakeJoints()
    if Pos then
        Model:MoveTo(Pos)
    end
    if Settings.AnchorParts then
        for i, v in ipairs(Model:GetDescendants()) do
            if v:IsA("BasePart") then
                v.Anchored = true
            end
        end
    end
    if Settings.RemoveDecals then
        for i, v in ipairs(Model:GetDescendants()) do
            if v:IsA("Decal") or v:IsA("Texture") then
                v:Destroy()
            end
        end
    end
    if Settings.RemoveScripts then
        for i, v in ipairs(Model:GetDescendants()) do
            if v:IsA("BaseScript") or v:IsA("ModuleScript") then
                v:Destroy()
            end
        end
    end
    Model.Parent = Parent or workspace
end

function InsertCloud:LoadAsset(url,key,id)
    if type(url) ~= "string" then
        return error("URL Parameter is invalid, must be a valid string")
    end
    if type(key) ~= "string" then
        return error("Key Parameter is invalid, must be a valid string")
    end
    
    Settings = Settings or _Settings.DefaultSettings
    Pos = Pos or _Settings.DefaultPos
    Parent = Parent or _Settings.DefaultParent
    
    id = tostring(id)
    
    local Model = Instance.new("Model")
    Model.Parent = Replicated
    Model.Name = id
    
    local New
    local request
    local FindCache = ServerCache:FindFirstChild(id)
    if FindCache==nil then
        New = url..key..id
        request = HTTPS:RequestAsync({
            Url = New,
            Method = 'GET',
            Headers = {},
        })
    else
        if Settings.LoadCache == true then
            Model:Destroy()
            local Clone = FindCache:Clone()
            InitModel(Clone, Parent, Pos, Settings)
            return Clone
        else
            New = url..key..id
            request = HTTPS:RequestAsync({
                Url = New,
                Method = 'GET',
                Headers = {},
            })
        end
    end
    if request.StatusCode==200 then
        local Response
        local Instances
        local Status, Error=pcall(function()
            --Pcall incase of error
            New = url..'/assets/v1/'..id
            request2 = HTTPS:RequestAsync({
                Url = New,
                Method = 'GET',
                Headers = {},
            })
            if request2.StatusCode==200 then
                local lxm = require(script.lxm)
                local asset = lxm(request2.Body)
                Instances = asset.Tree
                LoadModel(Model, Model, Instances)
                local XSum, XTot, ZSum, ZTot, YLow = 0, 0, 0, 0, math.huge
                local function GetCent(Par)
                    for i, v in ipairs(Par:GetChildren()) do
                        if v:IsA("BasePart") then
                            XTot = XTot + 1
                            ZTot = ZTot + 1
                            XSum = XSum + v.Position.X
                            ZSum = ZSum + v.Position.Z
                            if v.Position.Y - v.Size.Y / 2 < YLow then
                                YLow = v.Position.Y - v.Size.Y / 2
                            end
                        end
                        GetCent(v)
                    end
                end
                GetCent(Model)
                local Center = Instance.new("Part")
                Center.Parent = Model
                Center.Anchored = true
                Center.Locked = true
                Center.CanCollide = false
                Center.Transparency = 1
                Center.Size = Vector3.new(0.05, 0.05, 0.05)
                Center.Name = "CenterOfModel"
                Center.CFrame = CFrame.new(XSum / XTot, YLow, ZSum / ZTot)
                Model.PrimaryPart = Center
                local NewCache = Model:Clone()
                NewCache.Parent = ServerCache
                InitModel(Model, Parent, Pos, Settings)
            end
        end)
        
        if Status ~= true then
            Model:Destroy()
            return nil
        else
            if _Settings.CompileAssetAfterLoad then
                self:CompileAsset(Model)
            end
            return Model
        end
    end
end

function InsertCloud:CompileAsset(self, Model, Parent)
    pcall(function()
        Model.PrimaryPart:Destroy()
    end)
    Model:MakeJoints()
    for i, v in ipairs(Model:GetDescendants()) do
        if (v:IsA("Script") or v:IsA("LocalScript")) and v:FindFirstChild("IsDisabled") then
            pcall(function()
                v.Disabled = v.IsDisabled.Value
                v.IsDisabled:Destroy()
            end)
        end
    end
    local Children = Model:GetChildren()
    for i, v in ipairs(Children) do -- Ungroups model
        v.Parent = Parent or _Settings.DefaultCompileParent
    end
    Model:Destroy()
    return unpack(Children)
end

function InsertCloud:LoadCode(self, Code, Type, Parent, Player)
    local Script = Templates:FindFirstChild(SandboxType .. Type)
    Script = Script:Clone()
    if Script:FindFirstChild("Player") then
        Script.Player.Value = Player
    end
    Script.Parent = Parent or workspace
    Script.LOAD.Value = Code
    Script.Disabled = false
end
function InsertCloud:Credits(self)
    print("_DEVELOPERS:")
    for i, v in ipairs(self._DEVELOPERS) do
        print(v)
    end
end
function InsertCloud:RestartApp(self, URL, Key)
    URL = URL:sub(0, #URL - 8)
    HTTPS:GetAsync(URL .. "/restart/" .. Key)
end

return InsertCloud
