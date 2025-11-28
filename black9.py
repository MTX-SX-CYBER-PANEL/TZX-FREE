# By AbdeeLkarim BesTo

import requests , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading , random , os
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Key , Iv = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56]) , bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def EnC_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()
    
def DEc_AEs(HeX):
    cipher = AES.new(Key , AES.MODE_CBC , Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()
    
def EnC_PacKeT(HeX , K , V): 
    return AES.new(K , AES.MODE_CBC , V).encrypt(pad(bytes.fromhex(HeX) ,16)).hex()
    
def DEc_PacKeT(HeX , K , V):
    return unpad(AES.new(K , AES.MODE_CBC , V).decrypt(bytes.fromhex(HeX)) , 16).hex()  

def EnC_Uid(H , Tp):
    e , H = [] , int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0)) ; H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None

def EnC_Vr(N):
    if N < 0: ''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)
    
def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80: break
        s += 7
    return n
    
def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet    
    
def DecodE_HeX(H):
    R = hex(H) 
    F = str(R)[2:]
    if len(F) == 1: F = "0" + F ; return F
    else: return F

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None
                      
def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i + 3] for i in range(0 , len(str(n)) , 3))

def ArA_CoLor():
    Tp = ["32CD32" , "00BFFF" , "00FA9A" , "90EE90" , "FF4500" , "FF6347" , "FF69B4" , "FF8C00" , "FF6347" , "FFD700" , "FFDAB9" , "F0F0F0" , "F0E68C" , "D3D3D3" , "A9A9A9" , "D2691E" , "CD853F" , "BC8F8F" , "6A5ACD" , "483D8B" , "4682B4", "9370DB" , "C71585" , "FF8C00" , "FFA07A"]
    return random.choice(Tp)
    
def xBunnEr():
    bN = [902000306]
    return random.choice(bN)

def xSEndMsg(Msg , Tp , Tp2 , id , K , V):
    feilds = {1: id, 2: Tp2, 3: Tp, 4: Msg , 5: 1735129800, 7: 2, 9: {1: "xBesTo - C4­", 2: xBunnEr(), 3: 901048018, 4: 330, 5: 909034009, 8: "xBesTo - C4", 10: 1, 11: 1, 14: {1: 1158053040, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}}, 10: "en", 13: {2: 1, 3: 1}, 14: {}}
    Pk = str(CrEaTe_ProTo(feilds).hex())
    Pk = "080112" + EnC_Uid(len(Pk) // 2 , Tp = 'Uid') + Pk
    return GeneRaTePk(str(Pk) , '1215' , K , V)

def Auth_Chat(idT, sq, K, V):
    fields = {
        1: 3,
        2: {
            1: idT,
            3: "fr",
            4: sq
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1215' , K , V)
def xSendTeamMsg(msg, idT,  K, V):
    fields = {
    1: 1,
    2: {
        1: 12404281032,
        2: idT,
        4: msg,
        7: 2,
        10: "fr",
        9: {
            1: "C4 TEAM",
            2: xBunnEr(),
            4: 330,
            5: 827001005,
            8: "C4 TEAM",
            10: 1,
            11: 1,
            12: {
                1: 2
            },
            14: {
                1: 1158053040,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            }
        },
        13: {
            1: 2,
            2: 1
        },
        14:{}
    }
}
    
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1215' , K , V)

def OpEnSq(K , V):
    fields = {1: 1, 2: {2: "\u0001", 3: 1, 4: 1, 5: "en", 9: 1, 11: 1, 13: 1, 14: {2: 5756, 6: 11, 8: "1.111.5", 9: 2, 10: 4}}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def cHSq(Nu , Uid , K , V):
    fields = {1: 17, 2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 62, 5: "\u001a", 8: 5, 13: 329}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def SEnd_InV(Nu , Uid , K , V):
    fields = {1: 2 , 2: {1: int(Uid) , 2: "ME" , 4: int(Nu)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)
    
def ExiT(id , K , V):
    fields = {
        1: 7,
        2: {
            1: int(11037044965)
        }
        }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def AuthClan(CLan_Uid , AuTh , K , V):
    fields = {1: 3, 2: {1: int(CLan_Uid) , 2: 1, 4: str(AuTh)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1201' , K , V) 
        
def GeT_Status(PLayer_Uid , K , V):
    PLayer_Uid = EnC_Uid(PLayer_Uid , Tp = 'Uid')
    if len(PLayer_Uid) == 8: Pk = f'080112080a04{PLayer_Uid}1005'
    elif len(PLayer_Uid) == 10: Pk = f"080112090a05{PLayer_Uid}1005"
    return GeneRaTePk(Pk , '0f15' , K , V)
           
def SPam_Room(Uid , Rm , Nm , K , V):
    fields = {1: 78, 2: {1: int(Rm), 2: f"[{ArA_CoLor()}]{Nm}", 3: {2: 1, 3: 1}, 4: 330, 5: 1, 6: 201, 10: xBunnEr(), 11: int(Uid), 12: 1}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e15' , K , V)

def Join_Room(room_id , K , V):
    fields = {1: 3, 2: {1: int(room_id), 8: {1: "IDC1", 2: 3000, 3: "ME"}, 9: "\x01\t\n\x12\x19 ", 10: 1, 12: b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01", 13: 3, 14: 3, 16: "ME"}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0e10' , K , V)

def SPamSq(Uid , K , V): 
    fields = {1: 33, 2: {1: int(Uid) , 2: 'ME', 3: 1, 4: 1, 7: 330, 8: 19459, 9: 100, 12: 1, 16: 1, 17: {2: 94, 6: 11, 8: '1.111.5', 9: 3, 10: 2}, 18: 201, 23: {2: 1, 3: 1}, 24: xBunnEr() , 26: {}, 28: {}}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def AccEpT(PLayer_Uid , AuTh_CodE_Sq , K , V): 
    fields = {1: 4, 2: {1: int(PLayer_Uid), 3: int(PLayer_Uid), 4: "\u0001\u0007\t\n\u0012\u0019\u001a ", 8: 1, 9: {2: 1393, 4: "wW_T", 6: 11, 8: "1.111.5", 9: 3, 10: 2}, 10: AuTh_CodE_Sq, 12: 1, 13: "en", 16: "OR"}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def GenJoinSquadsPacket(code, key, iv):
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][4] = bytes.fromhex("01090a0b121920")
    fields[2][5] = str(code)
    fields[2][6] = 6
    fields[2][8] = 1
    fields[2][9] = {}
    fields[2][9][2] = 800
    fields[2][9][6] = 11
    fields[2][9][8] = "1.111.1"
    fields[2][9][9] = 5
    fields[2][9][10] = 1
    print(fields)
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', key, iv)
     #1750287629500765351_vfhkisb7hv 8679231987
def ghost_pakcet(player_id , nm , secret_code , key ,iv):
    fields = {
        1: 61,
        2: {
            1: int(player_id),  
            2: {
                1: int(player_id),  
                2: 1159,  
                3: f"[b][c][{ArA_CoLor()}]{nm}",  
                5: 12,  
                6: 15,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: secret_code,},}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', key, iv)
                                   
def _V(b, i):
    r = s = 0
    while True:
        c = b[i]; i += 1
        r |= (c & 0x7F) << s
        if c < 0x80: break
        s += 7
    return r, i

def PrOtO(hx):
    b, i, R = bytes.fromhex(hx), 0, {}
    while i < len(b):
        H, i = _V(b, i)
        F, T = H >> 3, H & 7
        if T == 0:
            R[F], i = _V(b, i)
        elif T == 2:
            L, i = _V(b, i)
            S = b[i:i+L]; i += L
            try: R[F] = S.decode()
            except:
                try: R[F] = PrOtO(S.hex())
                except: R[F] = S
        elif T == 5:
            R[F] = int.from_bytes(b[i:i+4], 'little'); i += 4
        else:
            raise ValueError(f'Unknown wire type: {T}')
    return R
    
def GeT_KEy(obj , target):
    values = []
    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == target:
                    values.append(v)
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)
    collect(obj)
    return values[-1] if values else None
 
 
def GeneRaTePk(Pk , N , K , V):
    PkEnc = EnC_PacKeT(Pk , K , V)
    _ = DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2: HeadEr = N + "000000"
    elif len(_) == 3: HeadEr = N + "00000"
    elif len(_) == 4: HeadEr = N + "0000"
    elif len(_) == 5: HeadEr = N + "000"
    return bytes.fromhex(HeadEr + _ + PkEnc)
    
def GuiLd_AccEss(Tg , Nm , Uid , BLk , OwN , AprV):
    return Tg in Nm and Uid not in BLk and Uid in (OwN | AprV)
            
def ChEck_Commande(id):
    return "<" not in id and ">" not in id and "[" not in id and "]" not in id
        
def L_DaTa():
    load = lambda f: json.load(open(f)) if os.path.exists(f) else {}
    return map(load, ["BesTo_CLan_LiKes.json" , "BesTo_RemaininG_LiKes.json" , "BesTo_RemaininG_Room.json"])
       
def ChEck_Limit_CLan(Uid , STaTus):
    data , max_use , file = (like_data_clan, 10, "BesTo_CLan_LiKes.json") if STaTus == "like" else ''
    t , limit = time.time(), 86400
    u = data.get(str(Uid), {"count": 0, "start_time": t})    
    if t - u["start_time"] >= limit:
        u = {"count": 0, "start_time": t}
    if u["count"] < max_use:
        u["count"] += 1
        data[str(Uid)] = u
        json.dump(data , open(file, "w"))
        return f"{max_use - u['count']}" , datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")
    return False , datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")

def ChEck_Limit(Uid , STaTus):
    data , max_use , file = (like_data, 10, "BesTo_RemaininG_LiKes.json") if STaTus == "like" else (room_data, 10, "BesTo_RemaininG_Room.json")
    t , limit = time.time(), 86400
    u = data.get(str(Uid), {"count": 0, "start_time": t})    
    if t - u["start_time"] >= limit:
        u = {"count": 0, "start_time": t}
    if u["count"] < max_use:
        u["count"] += 1
        data[str(Uid)] = u
        json.dump(data , open(file, "w"))
        return f"{max_use - u['count']}" , datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")
    return False , datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")
    
f = 'blacklist.txt'
approvee = 'approved.txt'
black , approve = [] , []

def load_blacklist():
    global black
    try: 
        with open(f, 'r') as file: 
            black = [line.strip() for line in file if line.strip()]
    except: black = []

def encrypt_uids():
    global black
    try: 
        if black: black = [EnC_Uid(uid , Tp = 'Uid') for uid in black]
    except: 
        try: open(f, 'w').close()
        except: pass
        load_blacklist()

if not black: open(f, 'w').close()

def load_approve():
    global approve
    try: 
        with open(approvee, 'r') as file: approve = [line.strip() for line in file if line.strip()]
    except: approve = []

def encrypt_uids2():
    global approve
    try: 
        if approve: approve = [EnC_Uid(uid , Tp = 'Uid') for uid in approve]
    except: 
        try: open(approvee, 'w').close()
        except: pass
        load_approve()

if not approve: open(approvee, 'w').close()
               
def Add_Uid(user_id):
    with open(f, 'r') as file: lines = file.read().splitlines()
    if str(user_id) not in lines:
        with open(f, 'a') as file: file.write(f"{user_id}\n")

def Remove_Uid(f, player_uid):
    try:
        with open(f, 'r+') as file: lines = file.readlines() ; file.seek(0), file.truncate(), file.writelines(l for l in lines if l.strip() != player_uid) ; return True
    except FileNotFoundError: return False
        
def A(user_id):
    with open(approvee, 'r') as file: lines = file.read().splitlines()
    if str(user_id) not in lines:
        with open(approvee, 'a') as file: file.write(f"{user_id}\n")

def D(approvee, player_uid):
    try:
        with open(approvee, 'r+') as file: lines = file.readlines() ; file.seek(0), file.truncate(), file.writelines(l for l in lines if l.strip() != player_uid) ; return True
    except FileNotFoundError: return False        

def Clear():
    try:
        open(f, 'w').close() ; black.clear() ; return True
    except: return False
                   
def Add_Black(user_id):
    Add_Uid(user_id)
    if EnC_Uid(user_id , Tp = 'Uid') not in black: black.append(EnC_Uid(user_id , Tp = 'Uid')) ; return True
    else: return False 
    
def Rem_Black(user_id):
    user_id_encrypted = EnC_Uid(user_id , Tp = 'Uid')
    if user_id_encrypted in black: black.remove(user_id_encrypted) ; Remove_Uid(f , user_id) ; return True
    else: return False       

def Show_Uids():
    try:
        with open(f) as file: return "\n".join(sorted(file.read().splitlines(), key=int)) or False
    except (FileNotFoundError, ValueError): return False 

def Approved(user_id):
    A(user_id)
    if EnC_Uid(user_id , Tp = 'Uid') not in approve: approve.append(EnC_Uid(user_id , Tp = 'Uid')) ; return True
    else: return False 
    
def DeApproved(user_id):
    user_id_encrypted = EnC_Uid(user_id , Tp = 'Uid')
    if user_id_encrypted in approve: approve.remove(user_id_encrypted) ; D(approvee , user_id) ; return True
    else: return False        
        
def Show_Approvs():
    try: 
        with open(approvee) as file: return "\n".join(sorted(file.read().splitlines(), key=int)) or False
    except (FileNotFoundError, ValueError): return False 
        
def Clear_Approvs():
    try: 
        open(approvee, 'w').close() ; approve.clear() ; return True
    except: return False
    
load_blacklist() ; encrypt_uids()    
load_approve() ; encrypt_uids2()   
like_data_clan , like_data , room_data = L_DaTa()