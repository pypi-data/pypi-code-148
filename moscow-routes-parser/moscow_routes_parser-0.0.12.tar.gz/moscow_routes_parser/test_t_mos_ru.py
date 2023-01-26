from datetime import date, time
from unittest import TestCase

from moscow_routes_parser.model import Route, Equipment
from moscow_routes_parser.model_impl import Timetable_builder_t_mos_ru
from moscow_routes_parser.t_mos_ru import Parser_routes_t_mos_ru, parser_timetable_t_mos_ru


class TestParser_routes_t_mos_ru(TestCase):
    def test_parse(self):
        parser = Parser_routes_t_mos_ru()
        routes = parser.parse(""""    <link rel="stylesheet" href="/build/map_schedule.79b35cf1.css">
<h1 class="">Расписания и&nbsp;схемы движения</h1>
<div class="tabs" data-id="schedule" data-type="ajax">

    <div class="container container_schedule">
        <div class="h3mb mob_select_big">
            <ul class="nav nav-pills nav-pills-big nav-select_js mt-8 mt_mob_-4 nav-schedule" role="tablist">
                <li class="nav-item">
                    <a data-type='all' class="nav-link  active " >Наземный транспорт</a>
                </li>
                <li class="nav-item">
                    <a data-type='aeroexpress' class="nav-link " href="/transport/schedule/aeroexpress">Аэроэкспресс</a>
                </li>
                                <li class="nav-item">
                    <a id="nav_night_bus" data-type='night'  class="nav-link " href="/transport/schedule/night">Ночные автобусы</a>
                </li>
            </ul>
        </div>
                <div class="d-md-none ">

            <div class="mt20md ">
                <div class="form-group form_btn_search form_btn_search2 w100p schedule_mb1">
                    <label for="schedule-search-bus12" class="btn_not_fon"><i class="icon-icons_search schedule-search-bus-submit" id="schedule-search-bus-submit"></i></label>
		    <div class="schedule-search-menu suggest-block" style="display: none;"></div>                    <input id="schedule-search-bus12" data-type="search-street" data-for="#mgt_schedule_search" type="text" class="form-control schedule-search-input" value="" placeholder="Поиск по номеру маршрута">
                </div>
            </div>
            <div class="d-flex justify-content-between mbrow schedule_mb2">
                <div>
                    <a class="filter-link" data-for="#mgt_schedule_direction" data-value="0">
                        <i class="ic ic-change-a-b" style="width: 2.2rem; height: 2.2rem;"></i>
                    </a>
                </div>
                <div>
                    <ul class="nav nav_a" role="tablist">
                        <li class="nav-item">
                            <a data-for="#mgt_schedule_workTime_0" class="nav-link active filter-link-nav" href="#" data-toggle="pill">Будни</a>
                        </li>
                        <li class="nav-item">
                            <a data-for="#mgt_schedule_workTime_1" class="nav-link filter-link-nav" href="#" data-toggle="pill">Выходные</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="pos_rel">
                    
<div class="tabs-nav tabs-nav--mobile tabs-nav--mb-half d-none">
    <div id="schedule-form" class="tabs-nav-inner">
                        <form name="mgt_schedule" method="get" class=" needs-validation" id="mgt_schedule_form">

            <div class="schedule-search-menu suggest-block" style="display: none;"></div>    <input type="text" id="mgt_schedule_search" name="mgt_schedule[search]" required="required" class="ajax-search form-control" data-ajax_url="/ru/ajax/App/SearchController/search" data-type="search-street" minlength="2" maxlength="256" data-for="App\Entity\Mgt\MgtRoute" data-suggest-container="#mgt_schedule_search_suggest" />

        <div class="empty-field-list"></div>
    <input type="hidden" id="mgt_schedule_isNight" name="mgt_schedule[isNight]" /><div class="form-group"><legend class="col-form-label">Filters</legend><div id="mgt_schedule_filters" class="ajax-change" data-type="schedule">
                    
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_filters_placeholder" name="mgt_schedule[filters]" class="form-check-input" value="" checked="checked" /><span class="sp_all"></span><span>All</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_filters_4" name="mgt_schedule[filters]" class="form-check-input" value="4" /><span class="sp_all"></span><span>Domodedovo</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_filters_5" name="mgt_schedule[filters]" class="form-check-input" value="5" /><span class="sp_all"></span><span>Sheremetevo</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_filters_6" name="mgt_schedule[filters]" class="form-check-input" value="6" /><span class="sp_all"></span><span>Vnukovo</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_filters_7" name="mgt_schedule[filters]" class="form-check-input" value="7" /><span class="sp_all"></span><span>Zhukovskiy</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_filters_8" name="mgt_schedule[filters]" class="form-check-input" value="8" /><span class="sp_all"></span><span>Stations</span></label>
                </div>            </div></div><div class="form-group"><legend class="col-form-label required">Work time</legend><div id="mgt_schedule_workTime" class="ajax-change" data-type="schedule" autocomplete="off">
                    
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_workTime_0" name="mgt_schedule[workTime]" required="required" class="form-check-input" value="1" checked="checked" /><span class="sp_all"></span><span>По будням</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_workTime_1" name="mgt_schedule[workTime]" required="required" class="form-check-input" value="0" /><span class="sp_all"></span><span>По выходным</span></label>
                </div>            </div></div><div class="form-group"><legend class="d-none col-form-label required">Direction</legend><div id="mgt_schedule_direction" class="ajax-change d-none" data-type="schedule" autocomplete="off">
                    
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_direction_0" name="mgt_schedule[direction]" required="required" class="form-check-input" value="0" checked="checked" /><span class="sp_all"></span><span>Прямой</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_direction_1" name="mgt_schedule[direction]" required="required" class="form-check-input" value="1" /><span class="sp_all"></span><span>Обратный</span></label>
                </div>            </div></div></form>

    </div>

</div>
<div class="tabs-content">
    <div class="tabs-content-item active" data-id="schedule-bus" data-parent="schedule">

        <div id="fix_thead_schedule" class="table-schedule table-schedule--mobile mini-ts--number table-night-route">
            <div class="table-schedule-thead">
                <div class="">
                    <div id="schedule-route-header" class="ts-header">
                        <div class="ts-number">
                            <div class="schedule-search">
                                <label for="schedule-search-bus">Маршрут <i class="ic ic-sm ic-search-grey"></i></label>
                                <div id="mgt_schedule_search_suggest" class="schedule-search-menu suggest-block" style="display: none;"></div>                                <input id="schedule-search-bus" data-for="#mgt_schedule_search" type="text" class="schedule-search-input schedule-search-input-desktop" data-type="search-street" maxlength="6" value="" placeholder="Найти номер" autocomplete="off">
                                <i id="schedule-search-close" class="icon icon-close-grey schedule-search-clear "></i>
                                                           </div>
                        </div>
                        <div class="ts-title">
                            <a class="filter-link" data-for="#mgt_schedule_direction" data-value="0">
                                Остановки <i class="ic ic-change-a-b" style="width: 16px; height: 16px;"></i>
                            </a>
                        </div>
                        <div class="ts-200">

                            <div class="dropdown days_filter">
                            <span data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="dropdown_text">По будням</span> <i class="ic ic-xs ic-expand-arrow-grey"></i></span>
                                <div class="dropdown-menu">
                                    <a class=" active  filter-link-one" href="#" data-for="#mgt_schedule_workTime_0">По будням</a>
                                    <a class=" filter-link-one" href="#" data-for="#mgt_schedule_workTime_1">По выходным</a>

                                </div>
                            </div>

                        </div>
                        <div class="ts-200">Интервал</div>
                    </div>

                </div>
            </div>
            <div id="schedule-table" class="ts-content js-schedule-scroll" data-current-page="1" data-count-pages="22">
                    <a class="ts-row "  href="/transport/schedule/route/1215">
    <div class="ts-number">
                    <i class="ic ic-bus"></i>
                З-27
    </div>
    <div class="ts-title">
        <span>
                            Западная - Деревня Назарьево
                    </span>
    </div>
    <div class="ts-200">
                                    с 06:00 по 20:45
                        </div>

    <div class="ts-200 tooltip-holder">
        <span class="tooltip-link">
             <span class="span_dotted">
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         каждые 20 - 60 мин
                              </span>
                            <span class="tooltip-wrap">
                    <span class="tooltip">
                        <table class="tooltip-table">
                            <tbody>
                                                              <tr>
                                    <td>6:00 - 7:00</td>
                                    <td>30 мин</td>
                                </tr>
                                                              <tr>
                                    <td>7:00 - 10:00</td>
                                    <td>20 мин</td>
                                </tr>
                                                              <tr>
                                    <td>10:00 - 13:00</td>
                                    <td>30 мин</td>
                                </tr>
                                                              <tr>
                                    <td>13:00 - 14:00</td>
                                    <td>60 мин</td>
                                </tr>
                                                              <tr>
                                    <td>14:00 - 15:00</td>
                                    <td>30 мин</td>
                                </tr>
                                                              <tr>
                                    <td>15:00 - 16:00</td>
                                    <td>20 мин</td>
                                </tr>
                                                              <tr>
                                    <td>16:00 - 17:00</td>
                                    <td>30 мин</td>
                                </tr>
                                                              <tr>
                                    <td>17:00 - 19:00</td>
                                    <td>20 мин</td>
                                </tr>
                                                              <tr>
                                    <td>19:00 - 21:00</td>
                                    <td>60 мин</td>
                                </tr>
                                                         </tbody>
                        </table>
                    </span>
                </span>
                    </span>


    </div>
</a>
    <a class="ts-row "  href="/transport/schedule/route/958">
    <div class="ts-number">
                    <i class="ic ic-bus"></i>
                З-28
    </div>
    <div class="ts-title">
        <span>
                            Станция Крюково - Пенсионный фонд
                    </span>
    </div>
    <div class="ts-200">
                                    с 05:10 по 00:38
                        </div>

    <div class="ts-200 tooltip-holder">
        <span class="tooltip-link">
             <span class="span_dotted">
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      каждые 10 - 30 мин
                              </span>
                            <span class="tooltip-wrap">
                    <span class="tooltip">
                        <table class="tooltip-table">
                            <tbody>
                                                              <tr>
                                    <td>0:00 - 1:00</td>
                                    <td>30 мин</td>
                                </tr>
                                                              <tr>
                                    <td>5:00 - 6:00</td>
                                    <td>20 мин</td>
                                </tr>
                                                              <tr>
                                    <td>6:00 - 7:00</td>
                                    <td>15 мин</td>
                                </tr>
                                                              <tr>
                                    <td>7:00 - 8:00</td>
                                    <td>10 мин</td>
                                </tr>
                                                              <tr>
                                    <td>8:00 - 9:00</td>
                                    <td>12 мин</td>
                                </tr>
                                                              <tr>
                                    <td>9:00 - 11:00</td>
                                    <td>20 мин</td>
                                </tr>
                                                              <tr>
                                    <td>11:00 - 13:00</td>
                                    <td>12 мин</td>
                                </tr>
                                                              <tr>
                                    <td>13:00 - 14:00</td>
                                    <td>10 мин</td>
                                </tr>
                                                              <tr>
                                    <td>14:00 - 16:00</td>
                                    <td>20 мин</td>
                                </tr>
                                                              <tr>
                                    <td>16:00 - 17:00</td>
                                    <td>15 мин</td>
                                </tr>
                                                              <tr>
                                    <td>17:00 - 19:00</td>
                                    <td>12 мин</td>
                                </tr>
                                                              <tr>
                                    <td>19:00 - 20:00</td>
                                    <td>15 мин</td>
                                </tr>
                                                              <tr>
                                    <td>20:00 - 23:00</td>
                                    <td>20 мин</td>
                                </tr>
                                                              <tr>
                                    <td>23:00 - 24:00</td>
                                    <td>15 мин</td>
                                </tr>
                                                         </tbody>
                        </table>
                    </span>
                </span>
                    </span>


    </div>
</a>
""")
        route1 = Route('1215', Equipment.bus(), 'З-27')
        route2 = Route('958', Equipment.bus(), 'З-28')
        self.assertEqual(routes, [route1, route2])


class Testparser_timetable_t_mos_ru(TestCase):
    def test_parse(self):
        parser = parser_timetable_t_mos_ru(Timetable_builder_t_mos_ru())
        timetable = parser.parse(""""

        <div class="pos_rel">
            <div class="h4fs mb10">
                <span id="schedule-route-header">
                    <span>Октябрьское трамвайное депо - Новоконная пл.</span>
                                    </span>
            </div>
                            <div class="h4fs h4mb">
                    <span id="schedule-route-worktime">
                                                                                    с 05:31
                                                                                                                                                                                                    по 00:54
                                                                                                    </span>
                </div>
                                        <form name="mgt_schedule" method="get" class=" needs-validation" id="mgt_schedule_form"><div id="mgt_schedule"><input type="hidden" id="mgt_schedule_isNight" name="mgt_schedule[isNight]" /><div class="form-group">                                        <div>
        <div class="pos_rel d-inline-block">
            <input type="text" id="mgt_schedule_date" name="mgt_schedule[date]" required="required" class="ajax-change datepicker form-control form-control is-invalid" data-type="schedule" data-toggle="datepicker" data-target="#mgt_schedule_date" value="12.03.2022" />
            <label class="icon-Calendar cal_ico" for="mgt_schedule_date"></label>
        </div>
    </div>
<div class="form-text invalid-text d-block"><div class="d-block">
                    Тип значения должен быть string.
                </div></div></div><input type="hidden" id="mgt_schedule_route" name="mgt_schedule[route]" value="393" /><div class="form-group"><legend class="d-none col-form-label required">Direction</legend><div id="mgt_schedule_direction" class="ajax-change d-none" data-type="schedule" autocomplete="off">
                    
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_direction_0" name="mgt_schedule[direction]" required="required" class="form-check-input" value="0" checked="checked" /><span class="sp_all"></span><span>Прямой</span></label>
                </div>                            
        <div class="form-check">                    <label class="label_input"><input type="radio" id="mgt_schedule_direction_1" name="mgt_schedule[direction]" required="required" class="form-check-input" value="1" /><span class="sp_all"></span><span>Обратный</span></label>
                </div>            </div></div></div><div class="empty-field-list"></div>
    </form>

            <div class="row mb72m">
                <div class="col-md-4 col-xl-3 order-2 order-md-1">
                    <div id="schedule-table">
                                                    <div class="schedule-route clearfix schedule-route--ru" data-coords="{&quot;type&quot;:&quot;FeatureCollection&quot;,&quot;features&quot;:[{&quot;id&quot;:6673,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.695663,55.735996]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041e\u043a\u0442\u044f\u0431\u0440\u044c\u0441\u043a\u043e\u0435 \u0442\u0440\u0430\u043c\u0432\u0430\u0439\u043d\u043e\u0435 \u0434\u0435\u043f\u043e&quot;,&quot;balloonContentHeader&quot;:&quot;\u041e\u043a\u0442\u044f\u0431\u0440\u044c\u0441\u043a\u043e\u0435 \u0442\u0440\u0430\u043c\u0432\u0430\u0439\u043d\u043e\u0435 \u0434\u0435\u043f\u043e&quot;}},{&quot;id&quot;:10894,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.687195,55.736732]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0440.&quot;}},{&quot;id&quot;:6759,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.684216,55.737026]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0412\u043e\u043b\u043e\u0432\u044c\u044f \u0443\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0412\u043e\u043b\u043e\u0432\u044c\u044f \u0443\u043b.&quot;}},{&quot;id&quot;:6758,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.675537,55.738037]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0411. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0411. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b.&quot;}},{&quot;id&quot;:6014,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.670345,55.735474]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\/\u0442 \&quot;\u041f\u043e\u0431\u0435\u0434\u0430\&quot; - \u0414\u0435\u0442\u0441\u043a\u0438\u0439 \u0442\u0435\u0430\u0442\u0440&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\/\u0442 \&quot;\u041f\u043e\u0431\u0435\u0434\u0430\&quot; - \u0414\u0435\u0442\u0441\u043a\u0438\u0439 \u0442\u0435\u0430\u0442\u0440&quot;}},{&quot;id&quot;:6675,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.66289,55.731194]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0440\u043e\u043b\u0435\u0442\u0430\u0440\u0441\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0440\u043e\u043b\u0435\u0442\u0430\u0440\u0441\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:6676,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.65948,55.730473]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0414\u0438\u043d\u0430\u043c\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0414\u0438\u043d\u0430\u043c\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b.&quot;}},{&quot;id&quot;:6677,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.650436,55.728424]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041d\u043e\u0432\u043e\u0441\u043f\u0430\u0441\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;,&quot;balloonContentHeader&quot;:&quot;\u041d\u043e\u0432\u043e\u0441\u043f\u0430\u0441\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;}},{&quot;id&quot;:6678,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.644974,55.729782]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\u043e\u0436\u0435\u0432\u043d\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0443\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\u043e\u0436\u0435\u0432\u043d\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0443\u043b.&quot;}},{&quot;id&quot;:1009111,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.639816,55.730297]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0438\u0439 \u0432\u043e\u043a\u0437\u0430\u043b&quot;,&quot;balloonContentHeader&quot;:&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0438\u0439 \u0432\u043e\u043a\u0437\u0430\u043b&quot;}},{&quot;id&quot;:7573,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.63541,55.7318]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:7574,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.631935,55.736416]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0412\u0438\u0448\u043d\u044f\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0412\u0438\u0448\u043d\u044f\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;}},{&quot;id&quot;:9356,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.629852,55.740463]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u0422\u0440\u0435\u0442\u044c\u044f\u043a\u043e\u0432\u0441\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u0422\u0440\u0435\u0442\u044c\u044f\u043a\u043e\u0432\u0441\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:7575,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.62983,55.74203]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041d\u043e\u0432\u043e\u043a\u0443\u0437\u043d\u0435\u0446\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041d\u043e\u0432\u043e\u043a\u0443\u0437\u043d\u0435\u0446\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:7576,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.63463,55.7443]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\u043e\u043c\u0438\u0441\u0441\u0430\u0440\u0438\u0430\u0442\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\u043e\u043c\u0438\u0441\u0441\u0430\u0440\u0438\u0430\u0442\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;}},{&quot;id&quot;:7577,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.64229,55.74994]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u042f\u0443\u0437\u0441\u043a\u0438\u0435 \u0432\u043e\u0440\u043e\u0442\u0430&quot;,&quot;balloonContentHeader&quot;:&quot;\u042f\u0443\u0437\u0441\u043a\u0438\u0435 \u0432\u043e\u0440\u043e\u0442\u0430&quot;}},{&quot;id&quot;:7578,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.64749,55.752697]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0412\u043e\u0440\u043e\u043d\u0446\u043e\u0432\u043e \u041f\u043e\u043b\u0435&quot;,&quot;balloonContentHeader&quot;:&quot;\u0412\u043e\u0440\u043e\u043d\u0446\u043e\u0432\u043e \u041f\u043e\u043b\u0435&quot;}},{&quot;id&quot;:14190,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.648537,55.756424]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\u0430\u0437\u0430\u0440\u043c\u0435\u043d\u043d\u044b\u0439 \u043f\u0435\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\u0430\u0437\u0430\u0440\u043c\u0435\u043d\u043d\u044b\u0439 \u043f\u0435\u0440.&quot;}},{&quot;id&quot;:7580,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.646465,55.75917]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041f\u043e\u043a\u0440\u043e\u0432\u0441\u043a\u0438\u0435 \u0412\u043e\u0440\u043e\u0442\u0430&quot;,&quot;balloonContentHeader&quot;:&quot;\u041f\u043e\u043a\u0440\u043e\u0432\u0441\u043a\u0438\u0435 \u0412\u043e\u0440\u043e\u0442\u0430&quot;}},{&quot;id&quot;:7581,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.642902,55.76315]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0411. \u0425\u0430\u0440\u0438\u0442\u043e\u043d\u044c\u0435\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0411. \u0425\u0430\u0440\u0438\u0442\u043e\u043d\u044c\u0435\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;}},{&quot;id&quot;:7582,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.638756,55.76463]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u0427\u0438\u0441\u0442\u044b\u0435 \u043f\u0440\u0443\u0434\u044b\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u0427\u0438\u0441\u0442\u044b\u0435 \u043f\u0440\u0443\u0434\u044b\&quot;&quot;}},{&quot;id&quot;:7583,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.641144,55.763065]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0411. \u0425\u0430\u0440\u0438\u0442\u043e\u043d\u044c\u0435\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0411. \u0425\u0430\u0440\u0438\u0442\u043e\u043d\u044c\u0435\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;}},{&quot;id&quot;:7584,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.645042,55.75944]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041f\u043e\u043a\u0440\u043e\u0432\u0441\u043a\u0438\u0435 \u0412\u043e\u0440\u043e\u0442\u0430&quot;,&quot;balloonContentHeader&quot;:&quot;\u041f\u043e\u043a\u0440\u043e\u0432\u0441\u043a\u0438\u0435 \u0412\u043e\u0440\u043e\u0442\u0430&quot;}},{&quot;id&quot;:7585,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.64779,55.756138]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\u0430\u0437\u0430\u0440\u043c\u0435\u043d\u043d\u044b\u0439 \u043f\u0435\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\u0430\u0437\u0430\u0440\u043c\u0435\u043d\u043d\u044b\u0439 \u043f\u0435\u0440.&quot;}},{&quot;id&quot;:7586,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.646866,55.753292]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0412\u043e\u0440\u043e\u043d\u0446\u043e\u0432\u043e \u041f\u043e\u043b\u0435&quot;,&quot;balloonContentHeader&quot;:&quot;\u0412\u043e\u0440\u043e\u043d\u0446\u043e\u0432\u043e \u041f\u043e\u043b\u0435&quot;}},{&quot;id&quot;:16121,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.641933,55.750046]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u042f\u0443\u0437\u0441\u043a\u0438\u0435 \u0432\u043e\u0440\u043e\u0442\u0430&quot;,&quot;balloonContentHeader&quot;:&quot;\u042f\u0443\u0437\u0441\u043a\u0438\u0435 \u0432\u043e\u0440\u043e\u0442\u0430&quot;}},{&quot;id&quot;:7587,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.6344,55.744434]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\u043e\u043c\u0438\u0441\u0441\u0430\u0440\u0438\u0430\u0442\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\u043e\u043c\u0438\u0441\u0441\u0430\u0440\u0438\u0430\u0442\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;}},{&quot;id&quot;:7588,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.630276,55.742577]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041d\u043e\u0432\u043e\u043a\u0443\u0437\u043d\u0435\u0446\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041d\u043e\u0432\u043e\u043a\u0443\u0437\u043d\u0435\u0446\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:9358,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.62963,55.74042]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u0422\u0440\u0435\u0442\u044c\u044f\u043a\u043e\u0432\u0441\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u0422\u0440\u0435\u0442\u044c\u044f\u043a\u043e\u0432\u0441\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:7589,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.631268,55.73666]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0412\u0438\u0448\u043d\u044f\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0412\u0438\u0448\u043d\u044f\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0435\u0440.&quot;}},{&quot;id&quot;:7590,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.63522,55.731564]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:1009112,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.639606,55.73016]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0438\u0439 \u0432\u043e\u043a\u0437\u0430\u043b&quot;,&quot;balloonContentHeader&quot;:&quot;\u041f\u0430\u0432\u0435\u043b\u0435\u0446\u043a\u0438\u0439 \u0432\u043e\u043a\u0437\u0430\u043b&quot;}},{&quot;id&quot;:6726,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.64539,55.72949]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\u043e\u0436\u0435\u0432\u043d\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0443\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\u043e\u0436\u0435\u0432\u043d\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0443\u043b.&quot;}},{&quot;id&quot;:6727,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.649708,55.728428]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041d\u043e\u0432\u043e\u0441\u043f\u0430\u0441\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;,&quot;balloonContentHeader&quot;:&quot;\u041d\u043e\u0432\u043e\u0441\u043f\u0430\u0441\u0441\u043a\u0438\u0439 \u043c\u043e\u0441\u0442&quot;}},{&quot;id&quot;:6728,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.659855,55.73042]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0414\u0438\u043d\u0430\u043c\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b\u0438\u0446\u0430&quot;,&quot;balloonContentHeader&quot;:&quot;\u0414\u0438\u043d\u0430\u043c\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b\u0438\u0446\u0430&quot;}},{&quot;id&quot;:7193,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.664093,55.731342]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0440\u043e\u043b\u0435\u0442\u0430\u0440\u0441\u043a\u0430\u044f\&quot;&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c\u0435\u0442\u0440\u043e \&quot;\u041f\u0440\u043e\u043b\u0435\u0442\u0430\u0440\u0441\u043a\u0430\u044f\&quot;&quot;}},{&quot;id&quot;:6024,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.67043,55.734715]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041a\/\u0442 \&quot;\u041f\u043e\u0431\u0435\u0434\u0430\&quot; - \u0414\u0435\u0442\u0441\u043a\u0438\u0439 \u0442\u0435\u0430\u0442\u0440&quot;,&quot;balloonContentHeader&quot;:&quot;\u041a\/\u0442 \&quot;\u041f\u043e\u0431\u0435\u0434\u0430\&quot; - \u0414\u0435\u0442\u0441\u043a\u0438\u0439 \u0442\u0435\u0430\u0442\u0440&quot;}},{&quot;id&quot;:6025,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.6729,55.738075]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0410\u0431\u0435\u043b\u044c\u043c\u0430\u043d\u043e\u0432\u0441\u043a\u0430\u044f \u0417\u0430\u0441\u0442\u0430\u0432\u0430&quot;,&quot;balloonContentHeader&quot;:&quot;\u0410\u0431\u0435\u043b\u044c\u043c\u0430\u043d\u043e\u0432\u0441\u043a\u0430\u044f \u0417\u0430\u0441\u0442\u0430\u0432\u0430&quot;}},{&quot;id&quot;:6762,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.675285,55.7379]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0411. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0411. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u0443\u043b.&quot;}},{&quot;id&quot;:6761,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.68357,55.7369]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u0412\u043e\u043b\u043e\u0432\u044c\u044f \u0443\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u0412\u043e\u043b\u043e\u0432\u044c\u044f \u0443\u043b.&quot;}},{&quot;id&quot;:10895,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.689682,55.73639]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041c. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0440.&quot;,&quot;balloonContentHeader&quot;:&quot;\u041c. \u041a\u0430\u043b\u0438\u0442\u043d\u0438\u043a\u043e\u0432\u0441\u043a\u0438\u0439 \u043f\u0440.&quot;}},{&quot;id&quot;:6729,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.69598,55.73579]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041e\u043a\u0442\u044f\u0431\u0440\u044c\u0441\u043a\u043e\u0435 \u0442\u0440\u0430\u043c\u0432\u0430\u0439\u043d\u043e\u0435 \u0434\u0435\u043f\u043e&quot;,&quot;balloonContentHeader&quot;:&quot;\u041e\u043a\u0442\u044f\u0431\u0440\u044c\u0441\u043a\u043e\u0435 \u0442\u0440\u0430\u043c\u0432\u0430\u0439\u043d\u043e\u0435 \u0434\u0435\u043f\u043e&quot;}},{&quot;id&quot;:6672,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;Point&quot;,&quot;coordinates&quot;:[37.696346,55.73376]},&quot;properties&quot;:{&quot;hintContent&quot;:&quot;\u041d\u043e\u0432\u043e\u043a\u043e\u043d\u043d\u0430\u044f \u043f\u043b.&quot;,&quot;balloonContentHeader&quot;:&quot;\u041d\u043e\u0432\u043e\u043a\u043e\u043d\u043d\u0430\u044f \u043f\u043b.&quot;}},{&quot;id&quot;:54113,&quot;type&quot;:&quot;Feature&quot;,&quot;geometry&quot;:{&quot;type&quot;:&quot;LineString&quot;,&quot;coordinates&quot;:[[37.6963284,55.7338017],[37.6964262,55.7337783],[37.6966422,55.7337334],[37.6966716,55.7337281],[37.6967015,55.733724],[37.696732,55.7337213],[37.6967627,55.73372],[37.6967935,55.73372],[37.6968242,55.7337213],[37.6968546,55.7337241],[37.6968846,55.7337281],[37.6969138,55.7337335],[37.6969423,55.7337402],[37.6969697,55.7337481],[37.696996,55.7337572],[37.6970209,55.7337674],[37.6970443,55.7337787],[37.6970661,55.733791],[37.6970861,55.7338042],[37.6971042,55.7338183],[37.6971202,55.7338331],[37.6971342,55.7338486],[37.6971403,55.7338565],[37.6971556,55.7338773],[37.6971556,55.7338773],[37.6974965,55.7343424],[37.6979178,55.7349093],[37.6983169,55.735445],[37.6983678,55.7355286],[37.6983678,55.7355286],[37.6983785,55.7355417],[37.6983829,55.7355534],[37.6983849,55.7355611],[37.6983858,55.7355688],[37.6983857,55.7355766],[37.6983844,55.7355843],[37.6983821,55.7355919],[37.6983788,55.7355994],[37.6983744,55.7356068],[37.698369,55.7356139],[37.6983626,55.7356208],[37.6983552,55.7356273],[37.6983471,55.7356335],[37.698338,55.7356394],[37.6983282,55.7356448],[37.6983176,55.7356497],[37.6983064,55.7356542],[37.6982947,55.7356582],[37.6982823,55.7356616],[37.6982696,55.7356645],[37.6982612,55.735666],[37.6981909,55.7356756],[37.6981909,55.7356756],[37.6973542,55.7357559],[37.6959704,55.7358997],[37.6952273,55.7359668],[37.6945533,55.7360276],[37.6941966,55.73606],[37.6941966,55.73606],[37.6938081,55.7360947],[37.6931688,55.7361554],[37.6921301,55.7362515],[37.6911451,55.7363466],[37.6902252,55.7364317],[37.68883,55.7365488],[37.6882082,55.7365996],[37.6872624,55.736675],[37.6869984,55.7366986],[37.6855464,55.7368333],[37.6844138,55.736931],[37.6842623,55.7369464],[37.683033,55.7370746],[37.6807945,55.7373273],[37.679995,55.73742],[37.679669,55.7374583],[37.6789611,55.7375445],[37.6758685,55.7379373],[37.6745544,55.7380966],[37.6745544,55.7380966],[37.6744618,55.7381078],[37.6744207,55.7381127],[37.6743617,55.7381219],[37.6743043,55.7381333],[37.6742484,55.7381469],[37.6741944,55.7381627],[37.6741424,55.7381806],[37.6740928,55.7382005],[37.674045,55.7382227],[37.6735639,55.73846],[37.6735639,55.73846],[37.6735433,55.7384687],[37.6735139,55.7384803],[37.6734823,55.738491],[37.6734514,55.7384999],[37.6734474,55.738501],[37.6734154,55.7385086],[37.6733827,55.738515],[37.6733784,55.7385158],[37.6733427,55.738521],[37.6733086,55.7385248],[37.6732698,55.7385274],[37.6732352,55.7385284],[37.6732005,55.7385281],[37.673196,55.738528],[37.6731615,55.7385262],[37.6731228,55.7385227],[37.673089,55.7385183],[37.6730538,55.7385122],[37.6730172,55.7385042],[37.6729858,55.7384959],[37.6729516,55.7384852],[37.6729226,55.7384745],[37.6728914,55.7384612],[37.6728652,55.7384483],[37.6728376,55.7384327],[37.672815,55.738418],[37.6727974,55.738405],[37.6727944,55.7384025],[37.6727787,55.7383886],[37.6727659,55.7383762],[37.6727625,55.7383725],[37.6727491,55.7383545],[37.6727491,55.7383545],[37.672352,55.737758],[37.671899,55.7370924],[37.671417,55.7364346],[37.6709756,55.7359007],[37.6706871,55.7355499],[37.6704366,55.7352814],[37.6703136,55.7351643],[37.6695969,55.7345552],[37.6690708,55.7341066],[37.6688238,55.7338948],[37.6688238,55.7338948],[37.6687401,55.7338354],[37.6684883,55.7336456],[37.6684449,55.7336181],[37.6684449,55.7336181],[37.6681398,55.7334246],[37.6675642,55.7330806],[37.6675642,55.7330806],[37.6675003,55.7330424],[37.6671814,55.7328515],[37.6668289,55.7326384],[37.6661751,55.7322331],[37.6659243,55.7320922],[37.6659243,55.7320922],[37.6657332,55.7319906],[37.6656387,55.7319437],[37.6655386,55.7319006],[37.6654335,55.7318616],[37.6653365,55.7318306],[37.6652006,55.7317872],[37.6648499,55.7316778],[37.6648499,55.7316778],[37.6646198,55.731606],[37.6645951,55.7315992],[37.6645951,55.7315992],[37.6642054,55.7314929],[37.6635892,55.7313327],[37.6632592,55.7312526],[37.662871,55.7311616],[37.6624006,55.731058],[37.6612826,55.7308088],[37.6612826,55.7308088],[37.6605418,55.7306444],[37.6590098,55.7303087],[37.6578331,55.73005],[37.6578331,55.73005],[37.6576503,55.73001],[37.6576503,55.73001],[37.6576068,55.7300015],[37.6565017,55.7297562],[37.6562353,55.7296961],[37.6560854,55.7296622],[37.6559128,55.7296181],[37.6557476,55.7295658],[37.6555912,55.7295055],[37.6554856,55.7294579],[37.6554228,55.7294294],[37.6543624,55.7289612],[37.653325,55.7285002],[37.6524654,55.728117],[37.6517018,55.7277812],[37.6514409,55.7276694],[37.6514409,55.7276694],[37.6513182,55.7276119],[37.6513182,55.7276119],[37.6512612,55.7275874],[37.6511407,55.727543],[37.6510956,55.7275332],[37.6510398,55.72753],[37.6510133,55.7275295],[37.6509868,55.7275303],[37.6509606,55.7275324],[37.6509347,55.7275357],[37.6509095,55.7275404],[37.6508851,55.7275462],[37.6508616,55.7275533],[37.6508394,55.7275614],[37.6508185,55.7275707],[37.6507991,55.7275809],[37.6507814,55.727592],[37.6507655,55.727604],[37.6507514,55.7276167],[37.6507394,55.72763],[37.6507295,55.7276439],[37.6507218,55.7276582],[37.6507163,55.7276729],[37.6507131,55.7276877],[37.6507122,55.7277027],[37.6507136,55.7277177],[37.6507173,55.7277325],[37.6507232,55.7277471],[37.6507315,55.7277613],[37.6507423,55.7277756],[37.6507606,55.7277966],[37.6510216,55.7280317],[37.6510558,55.7280669],[37.6510558,55.7280669],[37.6510784,55.7280902],[37.6510843,55.7281011],[37.6510857,55.7281041],[37.6510898,55.7281153],[37.6510907,55.7281184],[37.6510935,55.7281328],[37.6510942,55.7281442],[37.6510942,55.7281473],[37.651093,55.7281587],[37.6510925,55.7281618],[37.6510886,55.7281762],[37.6510825,55.7281903],[37.6510737,55.7282049],[37.6510691,55.7282109],[37.6510667,55.7282137],[37.6510584,55.7282221],[37.651052,55.7282275],[37.6510488,55.72823],[37.6510417,55.7282351],[37.6510301,55.7282421],[37.6510262,55.7282443],[37.6510176,55.7282486],[37.6510041,55.7282544],[37.6509897,55.7282596],[37.6509746,55.728264],[37.650919,55.7282785],[37.650919,55.7282785],[37.6508123,55.7283063],[37.6507346,55.7283254],[37.648713,55.7288196],[37.6462464,55.729428],[37.6444727,55.7298838],[37.6438656,55.7300455],[37.6427144,55.730357],[37.6427144,55.730357],[37.6426351,55.7303749],[37.6425822,55.730386],[37.6425282,55.7303956],[37.6424735,55.7304035],[37.6424181,55.7304098],[37.6423622,55.7304144],[37.642306,55.7304174],[37.6422495,55.7304187],[37.642193,55.7304184],[37.6421366,55.7304164],[37.6421223,55.7304156],[37.6420117,55.73041],[37.6420117,55.73041],[37.6417577,55.7303972],[37.6411381,55.7303548],[37.6403852,55.7303029],[37.6396279,55.7302485],[37.6389094,55.7301978],[37.6382081,55.7301488],[37.6374476,55.7300926],[37.6370191,55.7300643],[37.6370191,55.7300643],[37.6368669,55.7300516],[37.6368556,55.7300508],[37.6368443,55.7300504],[37.636833,55.7300503],[37.6368216,55.7300505],[37.6368104,55.7300511],[37.6367991,55.730052],[37.636788,55.7300532],[37.636777,55.7300548],[37.6367661,55.7300566],[37.6367555,55.7300588],[37.636745,55.7300614],[37.6367349,55.7300642],[37.6367249,55.7300673],[37.6367153,55.7300707],[37.636706,55.7300744],[37.6366971,55.7300783],[37.6366885,55.7300825],[37.6366804,55.730087],[37.6366727,55.7300917],[37.6366654,55.7300966],[37.6366586,55.7301017],[37.6366522,55.730107],[37.6366464,55.7301125],[37.6366411,55.7301182],[37.6366363,55.730124],[37.6366349,55.7301259],[37.6366018,55.7301719],[37.6366018,55.7301719],[37.6365953,55.7301842],[37.6365375,55.7302682],[37.6363042,55.7305698],[37.6361686,55.7307312],[37.6361686,55.7307312],[37.6360265,55.7309005],[37.6357759,55.7311723],[37.6357759,55.7311723],[37.6354812,55.7314939],[37.635392,55.7315943],[37.6353486,55.7316435],[37.6353107,55.7316958],[37.6352629,55.7317667],[37.6348533,55.732441],[37.634493,55.733051],[37.6343243,55.7333344],[37.6339347,55.7339414],[37.633462,55.7345718],[37.6330641,55.7350784],[37.6324038,55.735764],[37.6317385,55.7364353],[37.6316777,55.7364923],[37.6315696,55.7366101],[37.6314795,55.7367336],[37.6314258,55.7368175],[37.6310728,55.7374068],[37.6306966,55.7380488],[37.6304491,55.7384958],[37.6302382,55.7389236],[37.6301378,55.739187],[37.6300864,55.7393863],[37.6297654,55.7405482],[37.6297496,55.7406143],[37.6297496,55.7406143],[37.6297299,55.740697],[37.6297123,55.7408212],[37.6297123,55.7408212],[37.6297081,55.7408513],[37.6297158,55.7418],[37.6297224,55.7419174],[37.6297286,55.7419585],[37.6297436,55.7420092],[37.6297627,55.742062],[37.6297952,55.7421154],[37.6298327,55.7421648],[37.6298758,55.7422122],[37.629928,55.7422579],[37.6299853,55.7422989],[37.6300498,55.7423411],[37.6301296,55.7423884],[37.6302603,55.7424528],[37.6305191,55.7425728],[37.63099,55.7427944],[37.631395,55.7429752],[37.6315116,55.7430255],[37.6315757,55.7430526],[37.6316446,55.743077],[37.6317453,55.7431069],[37.6318773,55.7431418],[37.6320195,55.7431786],[37.6321768,55.7432187],[37.6325006,55.7432962],[37.6326432,55.7433336],[37.6326979,55.7433496],[37.63275,55.7433682],[37.6327989,55.7433894],[37.6336774,55.7438413],[37.6337277,55.7438675],[37.6346277,55.7444063],[37.6346277,55.7444063],[37.6348982,55.7445676],[37.6358775,55.745165],[37.6360606,55.7452791],[37.6360606,55.7452791],[37.6363344,55.745451],[37.6363344,55.745451],[37.6374212,55.7461274],[37.637877,55.7464353],[37.6382605,55.7467105],[37.6385865,55.746945],[37.6396619,55.7477053],[37.6401357,55.7480576],[37.6409672,55.7486632],[37.6410259,55.7487067],[37.6410259,55.7487067],[37.6411345,55.7487912],[37.641161,55.748812],[37.641161,55.748812],[37.6411649,55.7488151],[37.6411989,55.7488465],[37.6412388,55.7488936],[37.6413099,55.7489936],[37.6413382,55.7490408],[37.641382,55.749124],[37.6414204,55.7492052],[37.6414971,55.7493649],[37.6415096,55.7493896],[37.6415324,55.7494246],[37.6415613,55.7494594],[37.6422457,55.7502535],[37.6422712,55.7502802],[37.6422899,55.7502943],[37.6422899,55.7502943],[37.6423154,55.7503135],[37.6423707,55.7503428],[37.6424484,55.7503772],[37.6427567,55.7505053],[37.6429238,55.750571],[37.6429328,55.750574],[37.6429955,55.7505927],[37.6430425,55.7506038],[37.6430425,55.7506038],[37.6430612,55.7506083],[37.6435975,55.7507198],[37.6439184,55.7507719],[37.6440083,55.7507826],[37.6440692,55.7507871],[37.6441409,55.7507868],[37.6441872,55.7507842],[37.6442787,55.7507755],[37.6444368,55.7507599],[37.6445356,55.7507565],[37.6446228,55.7507584],[37.64471,55.7507681],[37.6448019,55.7507837],[37.644945,55.7508111],[37.6450858,55.7508417],[37.645166,55.7508633],[37.6452871,55.7509031],[37.6454967,55.750994],[37.6456993,55.7510869],[37.6458775,55.7511758],[37.645909,55.7511955],[37.6459486,55.7512308],[37.6460081,55.7512871],[37.6460711,55.751352],[37.6461248,55.7514116],[37.6461879,55.751481],[37.6464448,55.751781],[37.646739,55.752117],[37.6470915,55.7525119],[37.6473529,55.752801],[37.6474389,55.7529069],[37.6474389,55.7529069],[37.6476024,55.7531738],[37.6476024,55.7531738],[37.6478737,55.7536819],[37.6480423,55.7539886],[37.6484134,55.7546634],[37.6485552,55.7549636],[37.6486115,55.7550972],[37.6486422,55.7552001],[37.6487072,55.7554879],[37.6487335,55.7556878],[37.6487338,55.7557521],[37.6487201,55.7558209],[37.6487063,55.7558701],[37.6486707,55.755979],[37.6486523,55.7560249],[37.6486315,55.7560702],[37.6486015,55.7561201],[37.6485749,55.756162],[37.6483087,55.7564771],[37.6478454,55.7569589],[37.6474044,55.757476],[37.6471589,55.7577498],[37.6471288,55.7577898],[37.6470988,55.7578396],[37.6470621,55.7579183],[37.6470621,55.7579183],[37.6470434,55.7579584],[37.6470108,55.7580208],[37.6470108,55.7580208],[37.6468045,55.7584157],[37.6467446,55.7585573],[37.6466752,55.7586754],[37.6465331,55.7589044],[37.6462837,55.7593054],[37.6462837,55.7593054],[37.6462164,55.7594136],[37.646184,55.7594667],[37.6461693,55.7595025],[37.6461693,55.7595025],[37.6461218,55.7596183],[37.6460034,55.7599705],[37.645987,55.7600222],[37.645987,55.7600222],[37.6459735,55.7600649],[37.6459672,55.760261],[37.6459672,55.760261],[37.6459946,55.7604255],[37.6459994,55.7604622],[37.6460009,55.7605118],[37.645991,55.7605694],[37.6459731,55.7606264],[37.6459473,55.7606825],[37.6459139,55.7607372],[37.6458729,55.7607903],[37.6458246,55.7608415],[37.6458118,55.7608538],[37.6456282,55.7610311],[37.6448681,55.7617558],[37.6444799,55.7621136],[37.6443478,55.7622331],[37.6442921,55.7622791],[37.6442457,55.7623086],[37.644117,55.7623901],[37.6440114,55.7624492],[37.6437746,55.7625773],[37.6432315,55.762871],[37.6427126,55.7631359],[37.641639,55.7636806],[37.6408716,55.7640349],[37.639606,55.76462],[37.6394994,55.7646694],[37.6394994,55.7646694],[37.6394798,55.7646785],[37.6394587,55.7646883],[37.6394347,55.7646985],[37.6394093,55.7647077],[37.6393827,55.7647157],[37.6393551,55.7647226],[37.6393266,55.7647281],[37.6392975,55.7647324],[37.6392678,55.7647354],[37.6392378,55.7647371],[37.6392076,55.7647375],[37.6391775,55.7647365],[37.6391477,55.7647342],[37.6391182,55.7647306],[37.6390894,55.7647256],[37.6390613,55.7647194],[37.6390341,55.764712],[37.6390081,55.7647034],[37.6389834,55.7646938],[37.63896,55.764683],[37.6389383,55.7646712],[37.6389182,55.7646585],[37.6389,55.764645],[37.6388837,55.7646306],[37.6388695,55.7646157],[37.6388574,55.7646001],[37.6388475,55.764584],[37.6388398,55.7645676],[37.6388345,55.7645509],[37.6388315,55.764534],[37.6388309,55.764517],[37.6388327,55.7645],[37.6388368,55.7644831],[37.6388432,55.7644665],[37.638852,55.7644503],[37.6388629,55.7644344],[37.638876,55.7644191],[37.6388913,55.7644044],[37.6389085,55.7643905],[37.6389172,55.7643842],[37.6390062,55.7643216],[37.6390062,55.7643216],[37.6397699,55.763924],[37.6404594,55.7635725],[37.641222,55.7631691],[37.6414889,55.7630219],[37.6416467,55.7629312],[37.6417569,55.7628609],[37.6418555,55.7627946],[37.6420005,55.7626915],[37.6421525,55.7625871],[37.6425143,55.7623218],[37.6427718,55.76213],[37.6429468,55.7619928],[37.6431103,55.7618602],[37.6431579,55.761824],[37.6433082,55.7617],[37.6434408,55.7615696],[37.6435548,55.7614338],[37.643575,55.7614066],[37.6439339,55.760982],[37.6442627,55.760602],[37.6446585,55.7601065],[37.6446585,55.7601065],[37.6446805,55.7600855],[37.6447362,55.760031],[37.6447999,55.7599686],[37.6448265,55.7599443],[37.6448909,55.7598672],[37.6448909,55.7598672],[37.6450442,55.7596838],[37.6452722,55.7593874],[37.6452722,55.7593874],[37.6452941,55.759359],[37.6454214,55.7591916],[37.6454296,55.7591802],[37.6454296,55.7591802],[37.6454977,55.7590853],[37.6456584,55.758832],[37.6458701,55.7585263],[37.6459603,55.7583924],[37.6462331,55.7579705],[37.6462519,55.7579457],[37.6462519,55.7579457],[37.6463245,55.7578504],[37.6464261,55.7577544],[37.6464261,55.7577544],[37.6468053,55.7573961],[37.6471772,55.7570364],[37.6474135,55.7568112],[37.6475711,55.7566543],[37.6480385,55.7560637],[37.648138,55.7559148],[37.6481784,55.7558386],[37.6482118,55.7557698],[37.6482313,55.755695],[37.648245,55.755617],[37.6482518,55.7555796],[37.6482505,55.7555396],[37.6482422,55.7554989],[37.6482304,55.7554596],[37.6482139,55.7554046],[37.6481751,55.7552899],[37.6481128,55.7551103],[37.6479429,55.7547571],[37.6477753,55.7544065],[37.6477202,55.7542886],[37.6472897,55.7535659],[37.6470522,55.7531941],[37.6470522,55.7531941],[37.6468291,55.7528774],[37.6468291,55.7528774],[37.6466221,55.75258],[37.6459819,55.7517264],[37.6458136,55.7514847],[37.6457668,55.7514205],[37.6457435,55.7513956],[37.6456782,55.7513485],[37.6455896,55.7512942],[37.6455163,55.7512536],[37.6453637,55.7511758],[37.6452204,55.7511065],[37.6451168,55.7510528],[37.6450678,55.7510299],[37.645019,55.7510123],[37.6449782,55.7509992],[37.644834,55.7509699],[37.644663,55.7509366],[37.6443892,55.7508894],[37.6441802,55.7508569],[37.6438922,55.7508091],[37.6435358,55.7507438],[37.6430378,55.7506417],[37.6430108,55.7506353],[37.6430108,55.7506353],[37.6429682,55.7506252],[37.6429016,55.7506054],[37.6428893,55.7506012],[37.6427196,55.7505345],[37.6424098,55.7504058],[37.6423291,55.7503701],[37.6422677,55.7503376],[37.642239,55.750316],[37.642239,55.750316],[37.6422173,55.7502996],[37.6421889,55.7502698],[37.6415039,55.7494748],[37.6414736,55.7494385],[37.641449,55.7494008],[37.6414357,55.7493746],[37.6413589,55.7492145],[37.6413204,55.7491333],[37.6412491,55.7490043],[37.6411798,55.748907],[37.6411414,55.748862],[37.6411112,55.7488363],[37.6411112,55.7488363],[37.6410833,55.7488126],[37.640973,55.7487296],[37.640973,55.7487296],[37.6409169,55.7486852],[37.6400852,55.7480795],[37.6396121,55.7477277],[37.6385365,55.7469673],[37.6382104,55.7467327],[37.6378281,55.7464583],[37.637374,55.7461515],[37.6362847,55.7454756],[37.6362847,55.7454756],[37.6360064,55.7452989],[37.6360064,55.7452989],[37.6358305,55.7451892],[37.6348444,55.7445846],[37.6345894,55.744426],[37.6345894,55.744426],[37.6336816,55.7438923],[37.6336343,55.7438678],[37.6327834,55.7434343],[37.6327281,55.7434078],[37.6326663,55.743383],[37.6326009,55.7433612],[37.6325324,55.7433428],[37.6321512,55.7432516],[37.6319931,55.7432114],[37.6318501,55.7431743],[37.6317164,55.7431386],[37.6316132,55.7431083],[37.6315396,55.7430822],[37.6314732,55.7430541],[37.6313559,55.7430036],[37.6309499,55.7428223],[37.6304783,55.7426004],[37.6302191,55.7424802],[37.6300854,55.7424143],[37.6300026,55.7423652],[37.6299362,55.7423218],[37.6298761,55.7422788],[37.6298206,55.7422302],[37.629775,55.74218],[37.6297358,55.7421284],[37.6297011,55.7420715],[37.6296809,55.7420157],[37.6296653,55.741963],[37.6296588,55.7419194],[37.6296521,55.7418006],[37.6296444,55.7408499],[37.6296496,55.7408128],[37.6296496,55.7408128],[37.6296666,55.7406932],[37.6296863,55.7406106],[37.6296863,55.7406106],[37.6297024,55.7405431],[37.6300235,55.7393806],[37.630076,55.7391901],[37.6301762,55.7389153],[37.6303881,55.7384856],[37.630636,55.7380378],[37.6310124,55.7373954],[37.6313656,55.7368056],[37.6314201,55.7367206],[37.6315118,55.736595],[37.6316221,55.7364748],[37.6316829,55.7364178],[37.6323482,55.7357464],[37.6330059,55.7350638],[37.6334033,55.7345578],[37.6338748,55.7339291],[37.6342639,55.733323],[37.6344326,55.7330394],[37.634793,55.7324295],[37.6352033,55.7317541],[37.6352688,55.731662],[37.6352959,55.7316251],[37.6354243,55.7314778],[37.6357092,55.7311669],[37.6357092,55.7311669],[37.6360878,55.7307538],[37.6361159,55.7307197],[37.6361159,55.7307197],[37.6361379,55.730693],[37.6364782,55.7302551],[37.6365342,55.7301741],[37.6365412,55.7301613],[37.6365412,55.7301613],[37.6365832,55.7301058],[37.636588,55.7301],[37.6365932,55.7300943],[37.636599,55.7300887],[37.6366054,55.7300834],[37.6366122,55.7300782],[37.6366195,55.7300732],[37.6366272,55.7300685],[37.6366354,55.730064],[37.6366439,55.7300598],[37.6366528,55.7300558],[37.6366622,55.730052],[37.6366733,55.7300481],[37.6366836,55.7300446],[37.6366942,55.7300415],[37.6367051,55.7300387],[37.6367162,55.7300362],[37.6367276,55.730034],[37.6367391,55.7300322],[37.6367507,55.7300308],[37.6367625,55.7300296],[37.636769,55.7300292],[37.6367881,55.7300281],[37.6368073,55.7300275],[37.6368266,55.7300276],[37.6368458,55.7300282],[37.6368649,55.7300293],[37.636869,55.7300296],[37.6370244,55.7300426],[37.6370244,55.7300426],[37.6370282,55.730043],[37.6370482,55.7300447],[37.6370657,55.7300457],[37.6371485,55.7300498],[37.6376745,55.7300863],[37.6382155,55.7301251],[37.6389771,55.7301819],[37.639729,55.730232],[37.640881,55.7303126],[37.6419577,55.730386],[37.6420331,55.7303881],[37.6420331,55.7303881],[37.6422115,55.730393],[37.6422493,55.7303935],[37.642287,55.7303929],[37.6423247,55.7303911],[37.6423622,55.7303882],[37.6423993,55.7303843],[37.642436,55.7303792],[37.6424722,55.7303731],[37.6425078,55.7303659],[37.6425211,55.7303629],[37.6426827,55.7303256],[37.6426827,55.7303256],[37.6438133,55.7300193],[37.6444463,55.7298511],[37.6462209,55.7293951],[37.648688,55.7287865],[37.650709,55.7282926],[37.6507859,55.7282736],[37.6508906,55.7282463],[37.6508906,55.7282463],[37.6509462,55.7282318],[37.6509564,55.7282289],[37.6509662,55.7282256],[37.6509754,55.7282217],[37.6509839,55.7282174],[37.6509918,55.7282127],[37.6509989,55.7282077],[37.6510053,55.7282023],[37.6510107,55.7281966],[37.6510153,55.7281906],[37.6510157,55.7281899],[37.651022,55.7281791],[37.6510266,55.728168],[37.6510295,55.7281567],[37.6510306,55.7281454],[37.6510299,55.728134],[37.6510275,55.7281227],[37.6510234,55.7281115],[37.6510196,55.7281012],[37.651001,55.7280819],[37.651001,55.7280819],[37.650705,55.7278142],[37.6506844,55.7277906],[37.6506718,55.7277739],[37.6506619,55.7277567],[37.6506546,55.7277391],[37.6506501,55.7277211],[37.6506484,55.7277031],[37.6506495,55.727685],[37.6506534,55.727667],[37.65066,55.7276493],[37.6506694,55.7276319],[37.6506814,55.7276152],[37.6506959,55.727599],[37.6507129,55.7275836],[37.6507322,55.7275692],[37.6507536,55.7275557],[37.6507771,55.7275433],[37.6508024,55.7275322],[37.6508293,55.7275223],[37.6508576,55.7275138],[37.6508871,55.7275067],[37.6509176,55.7275011],[37.6509489,55.727497],[37.6509806,55.7274945],[37.6510127,55.7274935],[37.6510448,55.7274941],[37.6510766,55.7274963],[37.651108,55.7275],[37.6511387,55.7275053],[37.6511685,55.7275121],[37.6513023,55.7275604],[37.6513514,55.7275819],[37.6513514,55.7275819],[37.6514781,55.7276404],[37.6514781,55.7276404],[37.6517409,55.7277528],[37.6525046,55.7280887],[37.6533644,55.728472],[37.6544018,55.728933],[37.6554624,55.7294012],[37.6555904,55.7294593],[37.6557306,55.7295173],[37.6558792,55.7295682],[37.6560351,55.7296116],[37.6561241,55.7296323],[37.6565253,55.7297228],[37.6576734,55.7299783],[37.6576734,55.7299783],[37.6578511,55.7300161],[37.6578511,55.7300161],[37.6590328,55.7302752],[37.660565,55.7306109],[37.6613112,55.7307764],[37.6613112,55.7307764],[37.6636376,55.7312926],[37.6642199,55.731415],[37.6647296,55.7315203],[37.6647296,55.7315203],[37.6647612,55.7315268],[37.6650052,55.7315724],[37.6650052,55.7315724],[37.6651924,55.7316073],[37.6659258,55.7317168],[37.6664073,55.7317846],[37.6664073,55.7317846],[37.6664466,55.7317907],[37.6664948,55.7317975],[37.6666205,55.7318147],[37.6666777,55.7318238],[37.6667336,55.731835],[37.6667881,55.7318485],[37.6668407,55.731864],[37.6668913,55.7318816],[37.6669396,55.7319011],[37.6669853,55.7319225],[37.6670283,55.7319456],[37.6670683,55.7319704],[37.6671842,55.7320396],[37.6674855,55.7322697],[37.6676764,55.7324252],[37.6680227,55.7327408],[37.6681358,55.7328469],[37.6681358,55.7328469],[37.6688059,55.7334647],[37.6688059,55.7334647],[37.6688409,55.7334969],[37.6690977,55.7337822],[37.6690977,55.7337822],[37.6691184,55.7338023],[37.6697079,55.7343305],[37.6704773,55.7350134],[37.6706285,55.7351599],[37.6706941,55.7352335],[37.670758,55.7353292],[37.6708086,55.7354091],[37.6708688,55.7355058],[37.671015,55.7357771],[37.6711014,55.7359254],[37.6711896,55.7360473],[37.6714761,55.7364212],[37.6719582,55.737079],[37.672409,55.7377374],[37.6728002,55.7383308],[37.672804,55.7383362],[37.672804,55.7383362],[37.6728209,55.7383581],[37.6728331,55.73837],[37.6728481,55.7383832],[37.6728644,55.7383953],[37.6728857,55.7384091],[37.6729086,55.738422],[37.6729332,55.7384341],[37.6729591,55.7384451],[37.6729863,55.7384551],[37.6730147,55.7384639],[37.6730442,55.7384717],[37.6730745,55.7384782],[37.6731055,55.7384836],[37.6731372,55.7384877],[37.6731692,55.7384906],[37.6732016,55.7384922],[37.673234,55.7384925],[37.6732664,55.7384915],[37.6732987,55.7384893],[37.6733306,55.7384858],[37.6733619,55.738481],[37.6733926,55.7384751],[37.6734225,55.7384679],[37.6734514,55.7384596],[37.6734793,55.7384502],[37.6735058,55.7384396],[37.6735204,55.7384334],[37.6735204,55.7384334],[37.6740037,55.7381953],[37.6740542,55.7381719],[37.6741074,55.7381506],[37.6741632,55.7381314],[37.6742211,55.7381145],[37.6742811,55.7380998],[37.6743427,55.7380876],[37.6744056,55.7380778],[37.674449,55.7380726],[37.674581,55.7380566],[37.674581,55.7380566],[37.6758547,55.7379022],[37.6789474,55.7375094],[37.6796558,55.7374232],[37.679982,55.7373848],[37.6807818,55.7372921],[37.6830208,55.7370394],[37.6842463,55.7369116],[37.6843884,55.736899],[37.6855445,55.7367992],[37.6869881,55.7366632],[37.687253,55.7366395],[37.6881992,55.736564],[37.6888208,55.7365132],[37.6902154,55.7363962],[37.6911346,55.7363111],[37.6921196,55.736216],[37.6931583,55.7361199],[37.6937978,55.7360592],[37.6944836,55.7359969],[37.6944836,55.7359969],[37.694751,55.7359734],[37.6952644,55.735927],[37.6952644,55.735927],[37.6959596,55.7358643],[37.696709,55.735788],[37.696709,55.735788],[37.6967237,55.7357865],[37.6967292,55.7357858],[37.6967346,55.7357849],[37.6967398,55.7357838],[37.6967449,55.7357824],[37.6967498,55.7357808],[37.6967544,55.735779],[37.6967588,55.7357771],[37.6967628,55.7357749],[37.6967666,55.7357725],[37.69677,55.73577],[37.6967731,55.7357674],[37.6967758,55.7357646],[37.6967781,55.7357617],[37.69678,55.7357587],[37.6967815,55.7357556],[37.6967825,55.7357525],[37.6967831,55.7357494],[37.6967832,55.7357462],[37.696783,55.735743],[37.6967822,55.7357399],[37.6967809,55.7357364],[37.6967718,55.7357194],[37.6967718,55.7357194],[37.696624,55.7354433],[37.6959021,55.734144],[37.6959021,55.734144],[37.6958794,55.7340189],[37.6958782,55.7340076],[37.6958785,55.7339964],[37.6958803,55.7339852],[37.6958838,55.7339742],[37.6958887,55.7339633],[37.6958952,55.7339526],[37.6959031,55.7339423],[37.6959124,55.7339324],[37.6959231,55.7339229],[37.695935,55.7339139],[37.6959482,55.7339055],[37.6959625,55.7338977],[37.6959778,55.7338905],[37.6959941,55.733884],[37.6960113,55.7338783],[37.6960255,55.7338743],[37.6963284,55.7338017],[37.6963284,55.7338017],[37.6964262,55.7337783],[37.6966422,55.7337334],[37.6966716,55.7337281],[37.6967015,55.733724],[37.696732,55.7337213],[37.6967627,55.73372],[37.6967935,55.73372],[37.6968242,55.7337213],[37.6968546,55.7337241],[37.6968846,55.7337281],[37.6969138,55.7337335],[37.6969423,55.7337402],[37.6969697,55.7337481],[37.696996,55.7337572],[37.6970209,55.7337674],[37.6970443,55.7337787],[37.6970661,55.733791],[37.6970861,55.7338042],[37.6971042,55.7338183],[37.6971202,55.7338331],[37.6971342,55.7338486],[37.6971403,55.7338565],[37.6971556,55.7338773]]},&quot;properties&quot;:{&quot;id&quot;:54113}}],&quot;commonOptions&quot;:{&quot;strokeColor&quot;:&quot;#666666&quot;,&quot;strokeWidth&quot;:6,&quot;iconLayout&quot;:&quot;default#image&quot;,&quot;iconImageHref&quot;:&quot;\/build\/iconsf\/ico_blue.svg&quot;,&quot;iconImageSize&quot;:[20,22],&quot;iconImageOffset&quot;:[-10,-11]}}">
                                <span></span>
                                <ul>
                                                                            <li class=""
                                            data-direction="0"
                                            data-route="393"
                                            data-date="2022-03-12"
                                                                                            data-stop="0"
                                                                                            data-lang="">
                                            <div class="sl_a">
                                                <div class="krug_tochka
                                                                                                                                                                    krug_half
                                                                                                            ">
                                                </div>
                                                <div>
                                                                                                                                                            <div class="a_dotted d-inline">Октябрьское трамвайное депо</div>
                                                </div>
                                            </div>
                                            
                                            <div class="sl_collapse collapse">

                                                <div class="schedule_list_raspisanie">
                                                    <div class="raspisanie_data dt_thead">
                                                        <div class="dt1">ч</div>
                                                        <div class="dt2">мин</div>
                                                    </div>
                                                    <div class="raspisanie_hover">
                                                                                                                                                                            <div class="raspisanie_data ">
                                                                <div class="dt1"><strong>05:</strong></div>
                                                                <div class="dt2">
                                                                    <div class="raspisanie_data2">
                                                                                                                                                    <div>
                                                                                                                                                                <div class="div10" >
                                                                                    32
                                                                                </div>
                                                                            </div>
                                                                                                                                                    <div>
                                                                                                                                                                <div class="div10" >
                                                                                    52
                                                                                </div>
                                                                            </div>
                                                                                                                                            </div>
                                                                </div>
                                                            </div>
                                                                            <strong>
                                                                                <div style="color: red;" class="d-inline-block">Красные минуты:</div>
                                                                            </strong>
                                                                            специальный рейс Новоконная пл. - Метро &quot;Чистые пруды&quot;
                                                                        </div>
                                                                                                                                                                                                </div>
                                                                                                            </div>
                                                </div>
                                            </div>
                                        </li>
                                                                            <li class=""
                                            data-direction="0"
                                            data-route="393"
                                            data-date="2022-03-12"
                                                                                            data-stop="1"
                                                                                            data-lang="">
                                            <div class="sl_a">
                                                <div class="krug_tochka
                                                                                                                                                                    krug_half
                                                                                                            ">
                                                </div>
                                                <div>
                                                                                                                                                            <div class="a_dotted d-inline">М. Калитниковский пр.</div>
                                                </div>
                                            </div>
                                            
                                            <div class="sl_collapse collapse">

                                                <div class="schedule_list_raspisanie">
                                                    <div class="raspisanie_data dt_thead">
                                                        <div class="dt1">ч</div>
                                                        <div class="dt2">мин</div>
                                                    </div>
                                                    <div class="raspisanie_hover">
                                                                                                                    <div class="raspisanie_data ">
                                                                <div class="dt1"><strong>23:</strong></div>
                                                                <div class="dt2">
                                                                    <div class="raspisanie_data2">
                                                                                                                                                    <div>
                                                                                                                                                                <div class="div10"                                                                                                                                                                                                                                                                     style="color: red"
                                                                                        >
                                                                                    15
                                                                                </div>
                                                                            </div>
                                                                                                                                                    <div>
                                                                                                                                                                <div class="div10"                                                                                                                                                                                                                                                                     style="color: red"
                                                                                        >
                                                                                    35
                                                                                </div>
                                                                            </div>
                                                                                                                                                    <div>
                                                                                                                                                                <div class="div10"                                                                                                                                                                                                                                                                     style="color: red"
                                                                                        >
                                                                                    55
                                                                                </div>
                                                                            </div>
                                                                                                                                            </div>
                                                                </div>
                                                            </div>
                                                                                                                                                                            <div class="">
                                                                                                                                                                                                            <div>
                                                                            <strong>
                                                                                <div style="color: red;" class="d-inline-block">Красные минуты:</div>
                                                                            </strong>
                                                                            специальный рейс Новоконная пл. - Метро &quot;Чистые пруды&quot;
                                                                        </div>
                                                                                                                                                                                                </div>
                                                                                                            </div>
                                                </div>
                                            </div>
                                        </li>
                                                                            <li class=""
                                            data-direction="0"
                                            data-route="393"
                                            data-date="2022-03-12"
                                                                                            data-stop="2"
                                                                                            data-lang="">
                                            <div class="sl_a">
                                                <div class="krug_tochka
                                                                                                                                                                    krug_half
                                                                                                            ">
                                                </div>
""").set_date(date(2022, 2, 20)).set_direction(1).set_id_route_t_mos_ru('393').build()
        stop0 = timetable.get_stops()[0]
        stop1 = timetable.get_stops()[1]
        self.assertEqual(stop0.get_name(), "Октябрьское трамвайное депо")
        self.assertEqual(stop0.get_coords(), [37.695663, 55.735996])
        times0 = list(stop0.get_times())
        self.assertEqual(times0[0].get_time(), time(5, 32))
        self.assertEqual(times0[1].get_time(), time(5, 52))
        self.assertEqual(times0[0].get_color_special_flight(), None)
        self.assertEqual(times0[1].get_color_special_flight(), None)
        self.assertEqual(stop1.get_name(), "М. Калитниковский пр.")
        self.assertEqual(stop1.get_coords(), [37.687195, 55.736732])
        self.assertEqual(len(times0), 2)
        times1 = list(stop1.get_times())
        self.assertEqual(times1[0].get_time(), time(23, 15))
        self.assertEqual(times1[1].get_time(), time(23, 35))
        self.assertEqual(times1[2].get_time(), time(23, 55))
        self.assertEqual(times1[0].get_color_special_flight(), "red")
        self.assertEqual(times1[1].get_color_special_flight(), "red")
        self.assertEqual(times1[2].get_color_special_flight(), "red")
        self.assertEqual(len(times1), 3)
