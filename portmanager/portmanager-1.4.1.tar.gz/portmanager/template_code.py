IF_TABLE_SNMP_INDEX="""
<input id="id_snmp_index" value="{{ record.if_index }}" name="if_index" type="hidden" autocomplete="off">
"""


USERNAME = """
    {{ record.user.username }}
"""


DEVICE_GROUP_LINK = """
<a href="{% url 'plugins:portmanager:devicegroup' pk=record.pk %}">
    {{ record.name|default:'<span class="badge bg-info">Unnamed device</span>' }}
</a>
"""


DEVICE_LINK = """
<a href="{% url 'plugins:portmanager:device' pk=table.device_group_pk pk2=record.pk %}">
    {{ record.name|default:'<span class="badge bg-info">Unnamed device</span>' }}
</a>
"""


IF_TABLE_DESC = """
{% if record.if_enabled %}
  <input id="id_description" class="form-control" maxlength="180" value="{{ record.if_description }}" name="if_description" type="text" pattern="[ -ÿ]+" placeholder="Description" title="Description in ASCII format." autocomplete="off">
{% else %}
  <input id="id_description" class="form-control" maxlength="180" value="{{ record.if_description }}" name="if_description" type="text" placeholder="Description" title="Description in ASCII format." autocomplete="off" disabled>
  <input id="id_description" type="hidden" name="if_description" title="Description in ASCII format." value="{{ record.if_description }}" />
{% endif %}
"""


IF_TABLE_VLAN = """
{% load portmanager_filters %}
{% with act_vlan=table.vlans|keyvalue:record.if_vlan %}
{% if act_vlan is none %}
  <select id="id_vlan" name="if_vlan" class="netbox-static-select" autocomplete="off" required disabled>
    <option value=" " selected="selected" disabled>N/A</option>
  </select>
  <input id="id_vlan" type="hidden" name="if_vlan" value=""/>
{% elif not record.if_enabled %}
  <select id="id_vlan" name="if_vlan" class="netbox-static-select" autocomplete="off" required disabled>
    <option value="{{ act_vlan.vlan_index }}" selected="selected">{{ act_vlan.vlan_index }} {{ act_vlan.vlan_description }}</option>
  </select>
  <input id="id_vlan" type="hidden" name="if_vlan" value="" />
{% else %}
  <select id="id_vlan" name="if_vlan" class="netbox-static-select" autocomplete="off" required>
    <option value="{{ act_vlan.vlan_index }}" selected="selected">{{ act_vlan.vlan_index }} {{ act_vlan.vlan_description }}</option>
    {% for vlan_index, vlan in table.vlans.items %}
      {% if vlan.vlan_enabled and vlan.vlan_index != record.if_vlan %}
        <option value="{{ vlan.vlan_index }}">{{ vlan.vlan_index }} {{ vlan.vlan_description }}</option>
      {% endif %}
    {% endfor %}
  </select>
{% endif %}
{% endwith %}
<span class="ss-arrow">
  <span class="ss-arrow"></span>
</span>
"""


IF_TABLE_PS_MAX = """
{% load portmanager_filters %}
{% if record.if_enabled %}
  <input id="id_ps_max" size="1" class="form-control" value="{{ record.if_ps_max|getpsmax:record.if_ps_enable }}" name="if_ps_max" type="number" min="1" max="{{ table.portsec_max }}" placeholder="N/A" autocomplete="off"/>
{% else %}
  <input id="id_ps_max" size="1" class="form-control" value="{{ record.if_ps_max|getpsmax:record.if_ps_enable }}" name="if_ps_max" type="number" min="1" max="{{ table.portsec_max }}" placeholder="N/A" autocomplete="off" disabled/>
  <input id="id_ps_max" type="hidden" name="if_ps_max" value=""/>
{% endif %}
"""


IF_TABLE_ADMIN_STATUS = """
{% if record.if_enabled %}
  <select id="id_admin_status" name="if_admin_status" class="form-control" autocomplete="off" required>
    <option value="1" {% if record.if_admin_status == 1 %}selected="selected" {% endif %}>ON</option>
    <option value="2" {% if record.if_admin_status == 2 %}selected="selected" {% endif %}>OFF</option>
  </select>
{% else %}
  <select id="id_admin_status" name="if_admin_status" class="form-control" autocomplete="off" required disabled>
    <option value="record.if_admin_status" selected="selected" disabled>{% if record.if_admin_status == 1 %}ON{% else %}OFF{% endif %}</option>
  </select>
  <input id="id_admin_status" type="hidden" name="if_admin_status" value=""/>
{% endif %}
"""


IF_TABLE_STATE = """
{% load static %} 
{% if record.if_admin_status == 2 %}
  <img src="{% static 'portmanager/img/disabled.png'%}" alt="disabled" title="DISABLED" class="img-fluid" style="width:40px;">
{% elif record.if_oper_status == 1 %}
  <img src="{% static 'portmanager/img/connected.png'%}" alt="connected" title="CONNECTED" class="img-fluid" style="width:40px;">
{% else %}
  <img src="{% static 'portmanager/img/notconnected.png'%}" alt="notconnected" title="NOTCONNECTED" class="img-fluid" style="width:40px;">
{% endif %}
"""


IF_TABLE_SHOW_MACS="""
{% load helpers %}
{% if not record.if_enabled %}
<div class="btn-sm">show MACs</div>
{% else %}
<div class="btn btn-warning btn-sm"> 
  <a href="{% url 'plugins:portmanager:interface_mac' pk=table.device_group.pk pk2=table.device.pk pk3=record.if_index pk4=record.if_vlan %}">
    show MACs
  </a> 
</div>
{% endif %}
"""                 