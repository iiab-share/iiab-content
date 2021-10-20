#!/usr/bin/python3

import os, sys, syslog
import pwd, grp
import argparse
import iiab.iiab_lib as iiab
import iiab.adm_lib as adm

mod_path = adm.CONST.iiab_modules_dir
wasabi_mods = "wasabi-iiab-share:iiab-modules/"

def main():
    global mod_path
    mod_cat_frag = {
    "rating": "0.0",
    "age_range": "young adult, adult",
    "zip_ftp_url": "",
    "module_id": "IIAB", # we don't realy neeed an unique id
    "is_hidden": "No",
    "moddir": "",
    "category": "educational,technical",
    "title": "Put the title here",
    "prereq_id": None,
    "version": "1.0",
    "ksize": "0",
    "logo_url": None,
    "type": "html",
    "description": "Put a longer description here",
    "index_mod_sample_url": None,
    "source_url": "",
    "rsync_url": "",
    "rclone": "wasabi-iiab-share:iiab-modules/???",
    "lang": "en",
    "zip_http_url": "",
    "file_count": "0"
    }


    args = parse_args()
    mod_dir = args.mod_dir

    if args.path: # allow override of path
        mod_path = args.path



    # file_count = find <directory> -type f | wc -l
    # ksize = du -s

    mod_full_path = mod_path + mod_dir

    if not os.path.isdir(mod_full_path):
        print('Module directory '+ mod_full_path +' not found.')
        sys.exit(1)

    mod_cat_frag['moddir'] = mod_dir
    mod_cat_frag['lang'] = mod_dir.split('-')[0]

    try:
        menu_def = adm.read_json_file(adm.CONST.menu_def_dir + mod_dir + '.json')
        mod_cat_frag['title'] = menu_def['title']
        mod_cat_frag['description'] = menu_def['description']
    except:
        menu_def = {}

    mod_cat_frag['ksize'] = adm.subproc_cmd('du -s ' + mod_full_path).split('\t')[0]

    filecnt_cmd = 'find ' + mod_full_path + ' -type f'
    mod_file_list = adm.subproc_cmd(filecnt_cmd).split('\n')[:-1]
    mod_cat_frag['file_count'] = len (mod_file_list)

    mod_cat_frag['rclone'] =  wasabi_mods + mod_dir

    adm.write_json_file(mod_cat_frag, mod_dir + '.json')
    sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(description="Generate catalog json for a module. Uses Menu Definition if found.")
    parser.add_argument("mod_dir", help="The Module Name.")
    parser.add_argument("--path", help="Directory where module is located, default is " + mod_path)
    return parser.parse_args()

# Now start the application
if __name__ == "__main__":

    # Run the main routine
    main()
