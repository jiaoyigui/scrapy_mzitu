# scrapy mzitu 数据爬虫

---

## 版本说明

- version 0.1
    - [ ] 增量爬虫， 目前因数据量不大，直接使用使用url在mongodb中判断, 后期可切换成redis bloomfilter 过滤
    - [ ] 全部采集

## 使用学习
    - 全部采集 ``` scrapy crawl mzitu```
    - 增量采集 ``` scrapy crawl mzitu_inc```

## 采集频率
    - 每日1次