#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新聞爬取腳本
- 爬取 BBC News RSS feed 的最新 5 則新聞
- 更新 index.html 中的新聞區塊
- 作者：Grok 自動生成範例
- 執行環境：Python 3.8+
"""

import requests  # 用於 HTTP 請求
import xml.etree.ElementTree as ET  # 用於解析 RSS XML
from datetime import datetime  # 用於時間戳記
import re  # 用於簡單 HTML 清理

def fetch_bbc_news(num_items=5):
    """
    爬取 BBC 新聞 RSS
    Args:
        num_items (int): 爬取新聞數量
    Returns:
        list: 新聞項目清單，每項包含 HTML <li> 格式
    """
    rss_url = 'http://feeds.bbci.co.uk/news/rss.xml'  # BBC RSS 連結（國外新聞網站）
    
    try:
        # Step 1: 發送 GET 請求
        response = requests.get(rss_url, timeout=10)  # 設定 10 秒超時
        response.raise_for_status()  # 檢查 HTTP 錯誤
        
        # Step 2: 解析 XML
        root = ET.fromstring(response.content)
        
        # Step 3: 提取最新新聞項目
        items = []
        for item in root.findall('.//item')[:num_items]:  # 取前 num_items 則
            title_elem = item.find('title')
            link_elem = item.find('link')
            desc_elem = item.find('description')
            
            if title_elem is not None and link_elem is not None:
                title = title_elem.text or '無標題'
                link = link_elem.text or '#'
                desc = desc_elem.text[:100] + '...' if desc_elem is not None and desc_elem.text else '無描述'  # 截斷描述
                
                # Step 4: 清理描述中的 HTML 標籤（簡單版）
                desc = re.sub(r'<[^>]+>', '', desc)  # 移除 HTML 標籤
                
                # Step 5: 產生 HTML <li> 項目
                html_item = f'<li><a href="{link}" target="_blank">{title}</a>: {desc}</li>'
                items.append(html_item)
        
        return items
    
    except requests.exceptions.RequestException as e:
        print(f"請求錯誤：{e}")
        return []  # 錯誤時返回空清單
    except ET.ParseError as e:
        print(f"XML 解析錯誤：{e}")
        return []
    except Exception as e:
        print(f"未知錯誤：{e}")
        return []

def update_index_html(news_items):
    """
    更新 index.html 檔案
    - 替換 <div id="news"></div> 為新聞清單
    - 插入更新時間
    Args:
        news_items (list): 新聞 HTML 清單
    """
    try:
        # Step 1: 讀取現有 index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Step 2: 準備新聞 HTML
        if news_items:
            news_html = '<ul>' + ''.join(news_items) + '</ul>'
            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S (台灣時間)')
        else:
            news_html = '<p>無法載入新聞，請稍後再試。</p>'
            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S (台灣時間)')
        
        # Step 3: 替換內容
        # 替換新聞區塊
        html_content = html_content.replace('<div id="news"></div>', f'<div id="news">{news_html}</div>')
        # 替換更新時間（假設 HTML 有 <!-- 腳本會插入時間 --> 註解）
        html_content = html_content.replace('<!-- 腳本會插入時間 -->', update_time)
        
        # Step 4: 寫回檔案
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"更新完成！共 {len(news_items)} 則新聞，時間：{update_time}")
    
    except FileNotFoundError:
        print("錯誤：找不到 index.html 檔案，請確保在根目錄。")
    except Exception as e:
        print(f"更新檔案錯誤：{e}")

if __name__ == "__main__":
    # 主執行邏輯
    print("開始爬取 BBC 新聞...")
    news = fetch_bbc_news(5)  # 爬取 5 則
    update_index_html(news)
    print("腳本執行結束。")
