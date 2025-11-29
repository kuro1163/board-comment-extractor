#!/usr/bin/env python3
"""
掲示板まとめサイトからコメントを抽出してYouTube台本形式のスプレッドシートに変換するツール
"""

import re
import csv
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
from datetime import datetime

import click
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class CommentExtractor:
    """掲示板まとめサイトからコメントを抽出するクラス"""
    
    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.comments: List[Dict[str, str]] = []
        
    def fetch_html(self) -> Optional[str]:
        """HTMLを取得"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            click.echo(f"❌ HTML取得エラー: {e}", err=True)
            return None
    
    def extract_comments(self, html: str) -> List[Dict[str, str]]:
        """HTMLからコメントを抽出"""
        soup = BeautifulSoup(html, 'html.parser')
        comments = []
        seen_texts = set()  # 重複チェック用
        
        # あにまん掲示板専用の抽出ロジック
        if 'animanch.com' in self.domain:
            return self._extract_animanch_comments(soup, seen_texts)
        
        # パターン1: コメント番号（>>1, >>2など）を含む要素を検索
        numbered_pattern = re.compile(r'>>\d+')
        
        # コメント番号を含むテキストノードを検索
        for text_node in soup.find_all(string=numbered_pattern):
            parent = text_node.find_parent(['div', 'p', 'li', 'article', 'section'])
            if parent:
                text = parent.get_text(separator=' ', strip=True)
                if text and len(text) > 10 and text not in seen_texts:
                    seen_texts.add(text)
                    number_match = re.search(r'>>(\d+)', text)
                    comment_number = number_match.group(1) if number_match else None
                    
                    comments.append({
                        'number': comment_number or str(len(comments) + 1),
                        'speaker': self._extract_speaker(parent, text),
                        'text': text
                    })
        
        # パターン2: クラス名やIDにコメント関連のキーワードを含む要素
        comment_keywords = ['comment', 'res', 'post', 'message', 'reply', 'response']
        for keyword in comment_keywords:
            # クラス名で検索
            elements = soup.find_all(['div', 'p', 'li', 'article'], 
                                   class_=re.compile(keyword, re.I))
            for elem in elements:
                text = elem.get_text(separator=' ', strip=True)
                if text and len(text) > 10 and text not in seen_texts:
                    seen_texts.add(text)
                    number_match = re.search(r'>>(\d+)', text)
                    comment_number = number_match.group(1) if number_match else None
                    
                    comments.append({
                        'number': comment_number or str(len(comments) + 1),
                        'speaker': self._extract_speaker(elem, text),
                        'text': text
                    })
        
        # パターン3: ID属性で検索
        for elem in soup.find_all(['div', 'p', 'li'], id=re.compile(r'res|comment|post', re.I)):
            text = elem.get_text(separator=' ', strip=True)
            if text and len(text) > 10 and text not in seen_texts:
                seen_texts.add(text)
                number_match = re.search(r'>>(\d+)', text)
                comment_number = number_match.group(1) if number_match else None
                
                comments.append({
                    'number': comment_number or str(len(comments) + 1),
                    'speaker': self._extract_speaker(elem, text),
                    'text': text
                })
        
        # パターン4: 長いテキストを含む要素（フォールバック）
        if not comments:
            click.echo("⚠️  標準パターンでコメントが見つかりませんでした。フォールバック検索を実行します...")
            for elem in soup.find_all(['div', 'p', 'article']):
                text = elem.get_text(separator=' ', strip=True)
                # 20文字以上で、改行や句読点を含むテキストをコメント候補とする
                if (text and len(text) >= 20 and 
                    text not in seen_texts and
                    ('。' in text or '！' in text or '？' in text or '\n' in text)):
                    seen_texts.add(text)
                    number_match = re.search(r'>>(\d+)', text)
                    comment_number = number_match.group(1) if number_match else None
                    
                    comments.append({
                        'number': comment_number or str(len(comments) + 1),
                        'speaker': self._extract_speaker(elem, text),
                        'text': text
                    })
                    # フォールバックでは最大50件まで
                    if len(comments) >= 50:
                        break
        
        # コメント番号でソート（番号がある場合）
        comments_with_number = [c for c in comments if c['number'].isdigit()]
        comments_without_number = [c for c in comments if not c['number'].isdigit()]
        
        if comments_with_number:
            comments_with_number.sort(key=lambda x: int(x['number']))
        
        return comments_with_number + comments_without_number
    
    def _extract_animanch_comments(self, soup: BeautifulSoup, seen_texts: set) -> List[Dict[str, str]]:
        """あにまん掲示板専用のコメント抽出"""
        comments = []
        
        # IDがresで始まる要素を検索（res1, res2, res3など）
        for elem in soup.find_all(id=re.compile(r'^res\d+$')):
            # フォーム部分を除外
            if 'resform' in str(elem.get('class', [])):
                continue
            
            text = elem.get_text(separator=' ', strip=True)
            if not text or len(text) < 10:
                continue
            
            # IDからレス番号を取得（res1 -> 1）
            res_id = elem.get('id', '')
            res_number_match = re.search(r'res(\d+)', res_id)
            if not res_number_match:
                continue
            res_number = res_number_match.group(1)
            
            # 発言者名とコメント内容を抽出
            # パターン: "1スレ主25/11/29(土) 15:39:202報告"コメント内容"
            speaker_match = re.search(r'^\d+([^0-9]+?)\d{2}/\d{2}/\d{2}', text)
            if speaker_match:
                speaker_raw = speaker_match.group(1).strip()
                speaker = self._clean_animanch_speaker(speaker_raw)
            else:
                speaker = "匿名"
            
            # コメント内容を抽出（日付情報の後から）
            # 「報告」の後のテキストを取得
            report_match = re.search(r'報告(.+)$', text)
            if report_match:
                comment_text = report_match.group(1).strip()
            else:
                # 「報告」がない場合は、日付の後のテキストを取得
                date_match = re.search(r'\d{2}:\d{2}:\d{2}(.+)$', text)
                if date_match:
                    comment_text = date_match.group(1).strip()
                else:
                    # フォールバック: 最初の数字と日付を除いた部分
                    comment_text = re.sub(r'^\d+[^\d]+?\d{2}/\d{2}/\d{2}[^"]*', '', text).strip()
            
            # 空のコメントはスキップ
            if not comment_text or len(comment_text) < 5:
                continue
            
            # 重複チェック
            comment_key = f"{res_number}:{comment_text[:50]}"
            if comment_key in seen_texts:
                continue
            seen_texts.add(comment_key)
            
            comments.append({
                'number': res_number,
                'speaker': speaker,
                'text': comment_text
            })
        
        # レス番号でソート
        comments.sort(key=lambda x: int(x['number']) if x['number'].isdigit() else 9999)
        return comments
    
    def _clean_animanch_speaker(self, speaker_raw: str) -> str:
        """あにまん掲示板の発言者名をクリーンアップ"""
        # 日付パターンを除去（25/11/29(土) 15:39:20など）
        speaker = re.sub(r'\d{2}/\d{2}/\d{2}\(.*?\)\s+\d{2}:\d{2}:\d{2}', '', speaker_raw)
        speaker = speaker.strip()
        
        # 空の場合は「匿名」
        if not speaker:
            return "匿名"
        
        return speaker
    
    def _extract_speaker(self, element, text: str) -> str:
        """発言者名を抽出"""
        # パターン1: IDや名前が含まれている場合（より詳細なパターン）
        id_patterns = [
            r'ID[：:]\s*([^\s\n：:]+)',
            r'名前[：:]\s*([^\s\n：:]+)',
            r'投稿者[：:]\s*([^\s\n：:]+)',
            r'^([^：:\n]+)[：:]',  # 行頭の「名前：」パターン
            r'(\w+)[：:]\s*',  # 一般的な「名前：」パターン（最後に試行）
        ]
        
        for pattern in id_patterns:
            match = re.search(pattern, text)
            if match:
                speaker = match.group(1).strip()
                # 短すぎるものや数字のみは除外
                if len(speaker) > 1 and not speaker.isdigit():
                    return speaker
        
        # パターン2: 親要素からクラス名やIDを取得
        if hasattr(element, 'get'):
            # クラス名から抽出
            speaker_class = element.get('class', [])
            if speaker_class:
                for cls in speaker_class:
                    cls_lower = cls.lower()
                    if any(keyword in cls_lower for keyword in ['name', 'user', 'id', 'author', 'poster']):
                        # クラス名から実際の名前を抽出
                        name_match = re.search(r'([a-zA-Z0-9_]+)', str(cls))
                        if name_match:
                            return name_match.group(1)
            
            # ID属性から抽出
            speaker_id = element.get('id', '')
            if speaker_id:
                id_lower = speaker_id.lower()
                if any(keyword in id_lower for keyword in ['name', 'user', 'id', 'author', 'poster']):
                    name_match = re.search(r'([a-zA-Z0-9_]+)', speaker_id)
                    if name_match:
                        return name_match.group(1)
            
            # data属性から抽出
            for attr_name, attr_value in element.attrs.items():
                if any(keyword in attr_name.lower() for keyword in ['name', 'user', 'id', 'author']):
                    if isinstance(attr_value, str) and len(attr_value) > 1:
                        return attr_value
        
        # パターン3: テキスト内の最初の行から名前を推測
        first_line = text.split('\n')[0].split('：')[0].split(':')[0].strip()
        if len(first_line) > 1 and len(first_line) < 30 and not first_line.startswith('>>'):
            return first_line
        
        # パターン4: デフォルトは「匿名」
        return "匿名"
    
    def convert_to_script_format(self, comments: List[Dict[str, str]]) -> List[Tuple[str, str]]:
        """コメントを台本形式に変換"""
        script_lines = []
        
        for comment in comments:
            speaker = comment['speaker']
            text = comment['text']
            
            # テキストを適切な長さに分割（20-30字程度、最大50字）
            lines = self._split_text(text, max_length=50)
            
            for line in lines:
                script_lines.append((speaker, line))
        
        return script_lines
    
    def _split_text(self, text: str, max_length: int = 50) -> List[str]:
        """テキストを適切な長さに分割"""
        if len(text) <= max_length:
            return [text]
        
        lines = []
        current_line = ""
        
        # 句読点や改行で分割
        sentences = re.split(r'([。！？\n])', text)
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
            
            if len(current_line) + len(sentence) <= max_length:
                current_line += sentence
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = sentence
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines if lines else [text[:max_length]]
    
    def save_to_spreadsheet(self, script_lines: List[Tuple[str, str]], output_path: Path, format_type: str = 'tsv'):
        """スプレッドシート形式（TSV/CSV）で保存"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        delimiter = '\t' if format_type == 'tsv' else ','
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter, lineterminator='\n')
            
            # ヘッダー行
            writer.writerow(['発言者', 'セリフ'])
            
            # データ行
            for speaker, line in script_lines:
                writer.writerow([speaker, line])
        
        click.echo(f"✅ スプレッドシートを保存しました: {output_path}")


@click.command()
@click.argument('url', type=str)
@click.option('--output', '-o', type=click.Path(), default=None,
              help='出力ファイルパス（デフォルト: output/comments_YYYYMMDD_HHMMSS.tsv）')
@click.option('--format', 'output_format', type=click.Choice(['tsv', 'csv']), default='tsv',
              help='出力形式（tsv または csv、デフォルト: tsv）')
def main(url: str, output: Optional[str], output_format: str):
    """
    掲示板まとめサイトからコメントを抽出してYouTube台本形式のスプレッドシートに変換
    
    URL: 掲示板まとめサイトのURL
    """
    click.echo("🚀 コメント抽出を開始します...")
    
    # 出力パスの設定
    if output:
        output_path = Path(output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        extension = output_format
        output_path = output_dir / f"comments_{timestamp}.{extension}"
    
    # コメント抽出
    extractor = CommentExtractor(url)
    
    click.echo(f"📥 HTMLを取得中: {url}")
    html = extractor.fetch_html()
    
    if not html:
        click.echo("❌ HTMLの取得に失敗しました", err=True)
        sys.exit(1)
    
    click.echo("🔍 コメントを抽出中...")
    comments = extractor.extract_comments(html)
    
    if not comments:
        click.echo("⚠️  コメントが見つかりませんでした", err=True)
        click.echo("💡 ヒント: サイトの構造が想定と異なる可能性があります")
        sys.exit(1)
    
    click.echo(f"✅ {len(comments)}件のコメントを抽出しました")
    
    # 台本形式に変換
    click.echo("📝 台本形式に変換中...")
    script_lines = extractor.convert_to_script_format(comments)
    
    # スプレッドシートに保存
    click.echo("💾 スプレッドシートに保存中...")
    extractor.save_to_spreadsheet(script_lines, output_path, output_format)
    
    click.echo(f"\n✨ 完了！ {len(script_lines)}行の台本データを生成しました")
    click.echo(f"📊 ファイル: {output_path.absolute()}")


if __name__ == '__main__':
    main()

