import json
from pathlib import Path

def examine_pbip():
    report_dir = Path('output/PBIP/CMS_Organization_Determin.Report')
    pages_dir = report_dir / 'definition' / 'pages'
    
    with open('pbip_evidence.md', 'w', encoding='utf-8') as out:
        out.write('# PBIP Visual Generation Evidence\n\n')
        
        pages = list(pages_dir.glob('*'))
        for page_dir in pages:
            if not page_dir.is_dir(): continue
            page_id = page_dir.name
            
            page_json_path = page_dir / 'page.json'
            if page_json_path.exists():
                with open(page_json_path, 'r', encoding='utf-8') as f:
                    page_data = json.load(f)
                    out.write(f'## Page: {page_data.get("displayName", page_id)}\n')
                    out.write('### `page.json` Objects block:\n```json\n')
                    out.write(json.dumps(page_data.get('objects', {}), indent=2))
                    out.write('\n```\n\n')
            
            visuals_dir = page_dir / 'visuals'
            if not visuals_dir.exists():
                out.write('⚠️ **Missing `visuals` directory!**\n\n')
                continue
                
            visual_dirs = list(visuals_dir.glob('*'))
            out.write(f'Found {len(visual_dirs)} visual folders:\n\n')
            for v_dir in visual_dirs:
                if not v_dir.is_dir(): continue
                v_json_path = v_dir / 'visual.json'
                if not v_json_path.exists(): continue
                
                with open(v_json_path, 'r', encoding='utf-8') as f:
                    v_data = json.load(f)
                    v_type = v_data.get('visual', {}).get('visualType', 'unknown')
                    has_query = 'query' in v_data.get('visual', {})
                    has_prototype_query = 'prototypeQuery' in v_data.get('visual', {}).get('query', {})
                    
                    out.write(f'- Folder `{v_dir.name}` (`visualType`: **{v_type}**)\n')
                    out.write(f'  - Contains `query`: {has_query}\n')
                    out.write(f'  - Contains `prototypeQuery`: {has_prototype_query}\n\n')
                    
        version_file = report_dir / 'definition' / 'version.json'
        if version_file.exists():
            with open(version_file, 'r', encoding='utf-8') as f:
                version_data = json.load(f)
                out.write('## Version Mismatch Evidence\n')
                out.write('### `version.json` Contents:\n```json\n')
                out.write(json.dumps(version_data, indent=2))
                out.write('\n```\n')

if __name__ == '__main__':
    examine_pbip()
