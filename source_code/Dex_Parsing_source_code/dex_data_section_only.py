# s17orlax
# classes.dex로부터 data section만을 분리하여 [NAME]_data_section.dex 로 저장
# single-dex 파일만을 대상으로 함

import sys, os, zipfile, struct
def isdex(mm):
	if mm[0:3] == 'dex' and len(mm) > 0x70:
		return True
	return False
	
def header(mm):
	magic = mm[0:8]
	checksum = struct.unpack('<L', mm[8:0xC])[0]
	sal = mm[0xC:0x20]
	file_size = struct.unpack('<L', mm[0x20:0x24])[0]
	header_size = struct.unpack('<L', mm[0x24:0x28])[0]
	endian_tag = struct.unpack('<L', mm[0x28:0x2C])[0]
	link_size = struct.unpack('<L', mm[0x2C:0x30])[0]
	link_off = struct.unpack('<L', mm[0x30:0x34])[0]
	map_off = struct.unpack('<L', mm[0x34:0x38])[0]
	string_ids_size = struct.unpack('<L', mm[0x38:0x3C])[0]
	string_ids_off = struct.unpack('<L', mm[0x3C:0x40])[0]
	type_ids_size = struct.unpack('<L', mm[0x40:0x44])[0]
	type_ids_off = struct.unpack('<L', mm[0x44:0x48])[0]
	proto_ids_size = struct.unpack('<L', mm[0x48:0x4C])[0]
	proto_ids_off = struct.unpack('<L', mm[0x4C:0x50])[0]
	field_ids_size = struct.unpack('<L', mm[0x50:0x54])[0]
	field_ids_off = struct.unpack('<L', mm[0x54:0x58])[0]
	method_ids_size = struct.unpack('<L', mm[0x58:0x5C])[0]
	method_ids_off = struct.unpack('<L', mm[0x5C:0x60])[0]
	class_defs_size = struct.unpack('<L', mm[0x60:0x64])[0]
	class_defs_off = struct.unpack('<L', mm[0x64:0x68])[0]
	data_size = struct.unpack('<L', mm[0x68:0x6C])[0]
	data_off = struct.unpack('<L', mm[0x6C:0x70])[0]
	hdr = {}
	
	if len(mm) != file_size :
		return hdr
		
	hdr['magic'] = magic
	hdr['checksum'] = checksum
	hdr['sal'] = sal
	hdr['file_size'] = file_size
	hdr['header_size'] = header_size
	hdr['endian_tag'] = endian_tag
	hdr['link_size'] = link_size
	hdr['link_off'] = link_off
	hdr['map_off'] = map_off
	hdr['string_ids_size'] = string_ids_size
	hdr['string_ids_off'] = string_ids_off
	hdr['type_ids_size'] = type_ids_size
	hdr['type_ids_off'] = type_ids_off
	hdr['proto_ids_size'] = proto_ids_size
	hdr['proto_ids_off'] = proto_ids_off
	hdr['field_ids_size'] = field_ids_size
	hdr['field_ids_off'] = field_ids_off
	hdr['method_ids_size'] = method_ids_size
	hdr['method_ids_off'] = method_ids_off
	hdr['class_defs_size'] = class_defs_size
	hdr['class_defs_off'] = class_defs_off
	hdr['data_size'] = data_size
	hdr['data_off'] = data_off
	
	return hdr

def recursive_dir_cp(orig_dir,target_dir):
	for(path, dir, files) in os.walk(orig_dir):
		for dname in dir:
			if os.path.isdir(target_dir+(path+'\\'+dname).replace(orig_dir,'')):
				continue
			else:
				os.makedirs(target_dir+(path+'\\'+dname).replace(orig_dir,''))


if __name__ == "__main__":

	direc = 'D:\\Drebin\\apk_only'
	target_direc = 'D:\\Drebin\\data_section_dex'
	recursive_dir_cp(direc,target_direc)

	for (path, dir, files) in os.walk(direc):
		for fname in files:
			if os.path.splitext(fname)[-1] != ".apk":
				continue
			fullname = path + '\\' + fname
			try:
				tmp = zipfile.ZipFile(fullname)
			except:
				print (fullname + ' - Zipfile error')
				continue
			try:	# Check Multi-DEX
				tmp.extract('classes2.dex')
				print (fullname, " - Not Single Dex")
				os.remove('classes2.dex')
				continue
			except:
				pass
			try:
				tmp.extract('classes.dex')
			except:
				print(fullname, " - No Dex error")
				continue
			tmp.close()
			fp = open('classes.dex', 'rb')
			dexname = target_direc+fullname.replace(direc,'')+'_data_section.dex'
			#dexname = os.path.splitext(fname)[0]+'_data_section.dex'
			print( dexname)
			fp2 = open(dexname,'wb+')
			mm = fp.read()

			hdr = header(mm)
			data_off = hdr['data_off']
			fp.seek(data_off)
			fp2.write(fp.read())
			#fp3=open(dexname+'.dd','wb+')
			fp.seek(data_off)
			#fp3.write(fp.read(hdr['data_size']))
			#fp3.close()
			fp2.close()
			fp.close()

			if os.path.getsize(dexname) != hdr['data_size']:
				print("Size unmatched! - ",fullname)
			os.remove('classes.dex')
