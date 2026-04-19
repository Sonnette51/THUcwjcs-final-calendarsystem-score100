import React, { useState, useEffect } from 'react';
import { Calendar, Plus, Search, Edit2, Trash2, Star, ChevronLeft, ChevronRight } from 'lucide-react';

// 日期工具函数
const isLeapYear = (year) => {
  return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
};

const getDaysInMonth = (year, month) => {
  const daysInMonth = [31, isLeapYear(year) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return daysInMonth[month - 1];
};

const getWeekday = (year, month, day) => {
  // 蔡勒公式计算星期几
  let y = year, m = month;
  if (m < 3) {
    m += 12;
    y -= 1;
  }
  const c = Math.floor(y / 100);
  const yy = y % 100;
  const w = (yy + Math.floor(yy / 4) + Math.floor(c / 4) - 2 * c + Math.floor(26 * (m + 1) / 10) + day - 1) % 7;
  return (w + 7) % 7; // 0=Sunday, 1=Monday, ..., 6=Saturday
};

// 农历转换（简化版本）
const getLunarDate = (year, month, day) => {
  // 这里是简化实现，实际项目应使用完整的农历算法库
  const lunarMonths = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月'];
  const lunarDays = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
    '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
    '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'];
  
  // 简化计算：使用公历日期偏移估算
  const offset = ((year - 2000) * 365 + Math.floor((year - 2000) / 4) + 
    [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][month - 1] + day - 1) % 354;
  const lunarMonth = Math.floor(offset / 29.5) % 12;
  const lunarDay = Math.floor(offset % 29.5);
  
  return `${lunarMonths[lunarMonth]}${lunarDays[lunarDay]}`;
};

// 事件重复类型
const REPEAT_TYPES = {
  ONCE: 'once',
  DAILY: 'daily',
  WEEKLY: 'weekly',
  MONTHLY: 'monthly',
  YEARLY: 'yearly',
  CUSTOM: 'custom'
};

// 计算事件在指定日期是否发生（性能优化：使用数学计算而非遍历）
const eventOccursOnDate = (event, targetYear, targetMonth, targetDay) => {
  const startDate = new Date(event.startYear, event.startMonth - 1, event.startDay);
  const targetDate = new Date(targetYear, targetMonth - 1, targetDay);
  
  if (targetDate < startDate) return false;
  
  const daysDiff = Math.floor((targetDate - startDate) / (1000 * 60 * 60 * 24));
  
  switch (event.repeatType) {
    case REPEAT_TYPES.ONCE:
      return event.startYear === targetYear && 
             event.startMonth === targetMonth && 
             event.startDay === targetDay;
    
    case REPEAT_TYPES.DAILY:
      if (event.repeatCount && daysDiff >= event.repeatCount) return false;
      return true;
    
    case REPEAT_TYPES.WEEKLY:
      if (daysDiff % 7 !== 0) return false;
      const weekOccurrence = Math.floor(daysDiff / 7);
      if (event.repeatCount && weekOccurrence >= event.repeatCount) return false;
      return true;
    
    case REPEAT_TYPES.MONTHLY:
      let monthsDiff = (targetYear - event.startYear) * 12 + (targetMonth - event.startMonth);
      if (monthsDiff < 0) return false;
      if (event.repeatCount && monthsDiff >= event.repeatCount) return false;
      
      const targetMaxDay = getDaysInMonth(targetYear, targetMonth);
      const adjustedDay = Math.min(event.startDay, targetMaxDay);
      return targetDay === adjustedDay;
    
    case REPEAT_TYPES.YEARLY:
      const yearsDiff = targetYear - event.startYear;
      if (yearsDiff < 0) return false;
      if (event.repeatCount && yearsDiff >= event.repeatCount) return false;
      
      if (targetMonth !== event.startMonth) return false;
      
      if (event.startMonth === 2 && event.startDay === 29) {
        const maxDay = getDaysInMonth(targetYear, 2);
        return targetDay === maxDay;
      }
      return targetDay === event.startDay;
    
    case REPEAT_TYPES.CUSTOM:
      if (daysDiff % event.customInterval !== 0) return false;
      const customOccurrence = Math.floor(daysDiff / event.customInterval);
      if (event.repeatCount && customOccurrence >= event.repeatCount) return false;
      return true;
    
    default:
      return false;
  }
};

const CalendarEventSystem = () => {
  const [currentView, setCurrentView] = useState('menu');
  const [events, setEvents] = useState([]);
  const [selectedYear, setSelectedYear] = useState(2025);
  const [selectedMonth, setSelectedMonth] = useState(1);
  const [selectedDay, setSelectedDay] = useState(1);
  const [searchKeyword, setSearchKeyword] = useState('');
  
  // 从存储加载事件
  useEffect(() => {
    const loadEvents = async () => {
      try {
        const result = await window.storage.get('calendar-events');
        if (result && result.value) {
          setEvents(JSON.parse(result.value));
        }
      } catch (error) {
        console.log('No existing events');
      }
    };
    loadEvents();
  }, []);
  
  // 保存事件到存储
  const saveEvents = async (newEvents) => {
    setEvents(newEvents);
    try {
      await window.storage.set('calendar-events', JSON.stringify(newEvents));
    } catch (error) {
      console.error('Failed to save events:', error);
    }
  };
  
  // 添加事件
  const addEvent = (eventData) => {
    const newEvent = {
      id: Date.now(),
      ...eventData,
      createdAt: new Date().toISOString()
    };
    saveEvents([...events, newEvent]);
  };
  
  // 删除整个事件系列
  const deleteEventSeries = (eventId) => {
    saveEvents(events.filter(e => e.id !== eventId));
  };
  
  // 修改事件
  const updateEvent = (eventId, updates) => {
    saveEvents(events.map(e => e.id === eventId ? { ...e, ...updates } : e));
  };
  
  // 获取指定日期的事件
  const getEventsForDate = (year, month, day) => {
    return events.filter(event => eventOccursOnDate(event, year, month, day));
  };
  
  // 搜索事件
  const searchEvents = () => {
    if (!searchKeyword.trim()) return events;
    return events.filter(e => 
      e.name.includes(searchKeyword) || 
      (e.description && e.description.includes(searchKeyword))
    );
  };

  // 主菜单
  const MenuView = () => (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-center mb-6">日历事件管理系统</h2>
      <div className="grid grid-cols-1 gap-4">
        <button
          onClick={() => setCurrentView('calendar')}
          className="p-6 bg-blue-500 hover:bg-blue-600 text-white rounded-lg flex items-center justify-center gap-3 text-lg"
        >
          <Calendar size={24} />
          月历打印
        </button>
        <button
          onClick={() => setCurrentView('dateQuery')}
          className="p-6 bg-green-500 hover:bg-green-600 text-white rounded-lg flex items-center justify-center gap-3 text-lg"
        >
          <Search size={24} />
          日期信息查询
        </button>
        <button
          onClick={() => setCurrentView('eventManage')}
          className="p-6 bg-purple-500 hover:bg-purple-600 text-white rounded-lg flex items-center justify-center gap-3 text-lg"
        >
          <Edit2 size={24} />
          事件管理
        </button>
      </div>
    </div>
  );

  // 月历打印视图
  const CalendarView = () => {
    const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
    const firstDay = getWeekday(selectedYear, selectedMonth, 1);
    const daysInMonth = getDaysInMonth(selectedYear, selectedMonth);
    
    const calendar = [];
    let day = 1;
    
    for (let week = 0; week < 6; week++) {
      const weekDays = [];
      for (let weekday = 0; weekday < 7; weekday++) {
        if ((week === 0 && weekday < firstDay) || day > daysInMonth) {
          weekDays.push(null);
        } else {
          weekDays.push(day);
          day++;
        }
      }
      calendar.push(weekDays);
      if (day > daysInMonth) break;
    }
    
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between mb-4">
          <button onClick={() => setCurrentView('menu')} className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
            返回主菜单
          </button>
          <h2 className="text-xl font-bold">月历打印</h2>
          <div className="w-24"></div>
        </div>
        
        <div className="flex items-center justify-center gap-4 mb-4">
          <button onClick={() => setSelectedMonth(m => m === 1 ? 12 : m - 1)} className="p-2 hover:bg-gray-200 rounded">
            <ChevronLeft size={20} />
          </button>
          <div className="flex gap-2">
            <input
              type="number"
              value={selectedYear}
              onChange={(e) => setSelectedYear(Math.max(1, Math.min(9999, parseInt(e.target.value) || 2025)))}
              className="w-24 px-3 py-2 border rounded text-center"
              min="1"
              max="9999"
            />
            <span className="py-2">年</span>
            <input
              type="number"
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(Math.max(1, Math.min(12, parseInt(e.target.value) || 1)))}
              className="w-20 px-3 py-2 border rounded text-center"
              min="1"
              max="12"
            />
            <span className="py-2">月</span>
          </div>
          <button onClick={() => setSelectedMonth(m => m === 12 ? 1 : m + 1)} className="p-2 hover:bg-gray-200 rounded">
            <ChevronRight size={20} />
          </button>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg p-4">
          <div className="grid grid-cols-7 gap-2">
            {weekdays.map((day, idx) => (
              <div key={idx} className="text-center font-bold p-2 bg-gray-100 rounded">
                {day}
              </div>
            ))}
            {calendar.flat().map((day, idx) => {
              const hasEvents = day && getEventsForDate(selectedYear, selectedMonth, day).length > 0;
              return (
                <div
                  key={idx}
                  className={`text-center p-3 rounded min-h-12 ${
                    day ? 'bg-blue-50 hover:bg-blue-100 cursor-pointer' : ''
                  } ${hasEvents ? 'font-bold text-blue-600' : ''}`}
                  onClick={() => {
                    if (day) {
                      setSelectedDay(day);
                      setCurrentView('dateQuery');
                    }
                  }}
                >
                  {day || ''}
                  {hasEvents && <div className="text-xs text-red-500">●</div>}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  // 日期查询视图
  const DateQueryView = () => {
    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const weekday = getWeekday(selectedYear, selectedMonth, selectedDay);
    const lunar = getLunarDate(selectedYear, selectedMonth, selectedDay);
    const dayEvents = getEventsForDate(selectedYear, selectedMonth, selectedDay);
    
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between mb-4">
          <button onClick={() => setCurrentView('menu')} className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
            返回主菜单
          </button>
          <h2 className="text-xl font-bold">日期信息查询</h2>
          <div className="w-24"></div>
        </div>
        
        <div className="flex gap-2 justify-center items-center">
          <input
            type="number"
            value={selectedYear}
            onChange={(e) => setSelectedYear(Math.max(1, Math.min(9999, parseInt(e.target.value) || 2025)))}
            className="w-24 px-3 py-2 border rounded"
            min="1"
            max="9999"
          />
          <span>年</span>
          <input
            type="number"
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(Math.max(1, Math.min(12, parseInt(e.target.value) || 1)))}
            className="w-20 px-3 py-2 border rounded"
            min="1"
            max="12"
          />
          <span>月</span>
          <input
            type="number"
            value={selectedDay}
            onChange={(e) => setSelectedDay(Math.max(1, Math.min(getDaysInMonth(selectedYear, selectedMonth), parseInt(e.target.value) || 1)))}
            className="w-20 px-3 py-2 border rounded"
            min="1"
            max={getDaysInMonth(selectedYear, selectedMonth)}
          />
          <span>日</span>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg p-6 space-y-3">
          <div className="text-lg"><strong>星期：</strong>{weekdays[weekday]}</div>
          <div className="text-lg"><strong>农历：</strong>{lunar}</div>
          <div className="border-t pt-3 mt-3">
            <div className="text-lg font-bold mb-3">当天事件 ({dayEvents.length})</div>
            {dayEvents.length === 0 ? (
              <p className="text-gray-500">无事件</p>
            ) : (
              <div className="space-y-2">
                {dayEvents.map(event => (
                  <div key={event.id} className="p-3 bg-blue-50 rounded flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {event.starred && <Star size={16} className="text-yellow-500 fill-yellow-500" />}
                      <span className="font-medium">{event.name}</span>
                    </div>
                    <button
                      onClick={() => {
                        setCurrentView('eventDetail');
                      }}
                      className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
                    >
                      管理
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // 事件管理视图
  const EventManageView = () => {
    const [showAddForm, setShowAddForm] = useState(false);
    const [formData, setFormData] = useState({
      name: '',
      description: '',
      startYear: 2025,
      startMonth: 1,
      startDay: 1,
      repeatType: REPEAT_TYPES.ONCE,
      customInterval: 1,
      repeatCount: null,
      starred: false
    });
    
    const handleSubmit = () => {
      if (!formData.name.trim()) {
        alert('请输入事件名称');
        return;
      }
      addEvent(formData);
      setShowAddForm(false);
      setFormData({
        name: '',
        description: '',
        startYear: 2025,
        startMonth: 1,
        startDay: 1,
        repeatType: REPEAT_TYPES.ONCE,
        customInterval: 1,
        repeatCount: null,
        starred: false
      });
    };
    
    const filteredEvents = searchEvents();
    
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between mb-4">
          <button onClick={() => setCurrentView('menu')} className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
            返回主菜单
          </button>
          <h2 className="text-xl font-bold">事件管理</h2>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 flex items-center gap-2"
          >
            <Plus size={18} />
            添加事件
          </button>
        </div>
        
        {showAddForm && (
          <div className="bg-white rounded-lg shadow-lg p-6 space-y-4">
            <div>
              <label className="block mb-2 font-medium">事件名称 *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="w-full px-3 py-2 border rounded"
                required
              />
            </div>
            
            <div>
              <label className="block mb-2 font-medium">描述</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                className="w-full px-3 py-2 border rounded"
                rows="3"
              />
            </div>
            
            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="block mb-2 font-medium">年</label>
                <input
                  type="number"
                  value={formData.startYear}
                  onChange={(e) => setFormData({...formData, startYear: parseInt(e.target.value) || 2025})}
                  className="w-full px-3 py-2 border rounded"
                  min="1"
                  max="9999"
                />
              </div>
              <div>
                <label className="block mb-2 font-medium">月</label>
                <input
                  type="number"
                  value={formData.startMonth}
                  onChange={(e) => setFormData({...formData, startMonth: parseInt(e.target.value) || 1})}
                  className="w-full px-3 py-2 border rounded"
                  min="1"
                  max="12"
                />
              </div>
              <div>
                <label className="block mb-2 font-medium">日</label>
                <input
                  type="number"
                  value={formData.startDay}
                  onChange={(e) => setFormData({...formData, startDay: parseInt(e.target.value) || 1})}
                  className="w-full px-3 py-2 border rounded"
                  min="1"
                  max="31"
                />
              </div>
            </div>
            
            <div>
              <label className="block mb-2 font-medium">重复类型</label>
              <select
                value={formData.repeatType}
                onChange={(e) => setFormData({...formData, repeatType: e.target.value})}
                className="w-full px-3 py-2 border rounded"
              >
                <option value={REPEAT_TYPES.ONCE}>单次事件</option>
                <option value={REPEAT_TYPES.DAILY}>每日重复</option>
                <option value={REPEAT_TYPES.WEEKLY}>每周重复</option>
                <option value={REPEAT_TYPES.MONTHLY}>每月重复</option>
                <option value={REPEAT_TYPES.YEARLY}>每年重复</option>
                <option value={REPEAT_TYPES.CUSTOM}>自定义间隔</option>
              </select>
            </div>
            
            {formData.repeatType === REPEAT_TYPES.CUSTOM && (
              <div>
                <label className="block mb-2 font-medium">间隔天数</label>
                <input
                  type="number"
                  value={formData.customInterval}
                  onChange={(e) => setFormData({...formData, customInterval: parseInt(e.target.value) || 1})}
                  className="w-full px-3 py-2 border rounded"
                  min="1"
                />
              </div>
            )}
            
            {formData.repeatType !== REPEAT_TYPES.ONCE && (
              <div>
                <label className="block mb-2 font-medium">重复次数（留空表示无限重复）</label>
                <input
                  type="number"
                  value={formData.repeatCount || ''}
                  onChange={(e) => setFormData({...formData, repeatCount: e.target.value ? parseInt(e.target.value) : null})}
                  className="w-full px-3 py-2 border rounded"
                  min="1"
                  placeholder="无限重复"
                />
              </div>
            )}
            
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="starred"
                checked={formData.starred}
                onChange={(e) => setFormData({...formData, starred: e.target.checked})}
                className="w-4 h-4"
              />
              <label htmlFor="starred" className="flex items-center gap-1">
                <Star size={16} className="text-yellow-500" />
                标记为重要
              </label>
            </div>
            
            <div className="flex gap-2">
              <button onClick={handleSubmit} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                保存事件
              </button>
              <button
                onClick={() => setShowAddForm(false)}
                className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
              >
                取消
              </button>
            </div>
          </div>
        )}
        
        <div>
          <input
            type="text"
            value={searchKeyword}
            onChange={(e) => setSearchKeyword(e.target.value)}
            placeholder="搜索事件关键词..."
            className="w-full px-4 py-2 border rounded mb-4"
          />
        </div>
        
        <div className="space-y-2">
          <h3 className="font-bold text-lg">所有事件 ({filteredEvents.length})</h3>
          {filteredEvents.length === 0 ? (
            <p className="text-gray-500">暂无事件</p>
          ) : (
            filteredEvents.map(event => (
              <div key={event.id} className="bg-white rounded-lg shadow p-4 flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    {event.starred && <Star size={18} className="text-yellow-500 fill-yellow-500" />}
                    <span className="font-bold text-lg">{event.name}</span>
                  </div>
                  {event.description && <p className="text-gray-600 mb-2">{event.description}</p>}
                  <div className="text-sm text-gray-500">
                    <div>开始日期: {event.startYear}年{event.startMonth}月{event.startDay}日</div>
                    <div>重复: {
                      {
                        [REPEAT_TYPES.ONCE]: '单次',
                        [REPEAT_TYPES.DAILY]: '每日',
                        [REPEAT_TYPES.WEEKLY]: '每周',
                        [REPEAT_TYPES.MONTHLY]: '每月',
                        [REPEAT_TYPES.YEARLY]: '每年',
                        [REPEAT_TYPES.CUSTOM]: `每${event.customInterval}天`
                      }[event.repeatType]
                    }
                    {event.repeatCount ? ` (共${event.repeatCount}次)` : ' (无限)'}</div>
                  </div>
                </div>
                <button
                  onClick={() => {
                    if (window.confirm('确定要删除整个事件系列吗？')) {
                      deleteEventSeries(event.id);
                    }
                  }}
                  className="px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600 flex items-center gap-1"
                >
                  <Trash2 size={16} />
                  删除
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <div className="max-w-4xl mx-auto">
        {currentView === 'menu' && <MenuView />}
        {currentView === 'calendar' && <CalendarView />}
        {currentView === 'dateQuery' && <DateQueryView />}
        {currentView === 'eventManage' && <EventManageView />}
      </div>
    </div>
  );
};

export default CalendarEventSystem;