import libs.home_assistant
import logging


def on_off(entity_id, value):
    etype = entity_id.split(".")[0]
    match etype:
        case 'light' | 'switch' | 'input_boolean' | 'automation' | 'fan':
            service = "turn_off"
            if value == "1":
                service = "turn_on"
            libs.home_assistant.call_service(
                entity_name=entity_id,
                domain=etype,
                service=service,
                service_data={}
            )
        case _:
            logging.error(
                "Control action on_off not implemented for %s", entity_id)


def button_press(entity_id, value):
    etype = entity_id.split["."][0]
    match etype:
        case 'scene':
            libs.home_assistant.call_service(
                entity_name=entity_id,
                domain="scene",
                service="turn_on",
                service_data={}
            )

    # apis.ha_api.log(
    #     f"Button Press Event; entity_id: {entity_id}; button_type: {button_type}; value: {value} ")
    #  # buttons with actions on HA
    #  if button_type == "OnOff":
    #      if value == "1":
    #          apis.ha_api.turn_on(entity_id)
    #      else:
    #          apis.ha_api.turn_off(entity_id)
    #
    #  if button_type == "number-set":
    #      if entity_id.startswith('fan'):
    #          entity = apis.ha_api.get_entity(entity_id)
    #          value = float(value) * \
    #              float(entity.attributes.get("percentage_step", 0))
    #          entity.call_service("set_percentage", percentage=value)
    #      else:
    #          apis.ha_api.get_entity(entity_id).call_service(
    #              "set_value", value=value)
    #
    #  # for shutter / covers
    #  if button_type == "up":
    #      apis.ha_api.get_entity(entity_id).call_service("open_cover")
    #  if button_type == "stop":
    #      apis.ha_api.get_entity(entity_id).call_service("stop_cover")
    #  if button_type == "down":
    #      apis.ha_api.get_entity(entity_id).call_service("close_cover")
    #  if button_type == "positionSlider":
    #      pos = int(value)
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "set_cover_position", position=pos)
    #  if button_type == "tiltOpen":
    #      apis.ha_api.get_entity(entity_id).call_service("open_cover_tilt")
    #  if button_type == "tiltStop":
    #      apis.ha_api.get_entity(entity_id).call_service("stop_cover_tilt")
    #  if button_type == "tiltClose":
    #      apis.ha_api.get_entity(entity_id).call_service("close_cover_tilt")
    #  if button_type == "tiltSlider":
    #      pos = int(value)
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "set_cover_tilt_position", tilt_position=pos)
    #
    #  if button_type == "button":
    #      if entity_id.startswith('navigate'):
    #          # internal navigation for next/prev
    #          if entity_id.startswith('navigate.uuid'):
    #              dstCard = self._config.get_card_by_uuid(
    #                  entity_id.replace('navigate.', ''))
    #          # internal for navigation to nested pages
    #          else:
    #              dstCard = self._config.search_card(entity_id)
    #          if dstCard is not None:
    #              if dstCard.hidden:
    #                  self._previous_cards.append(self._current_card)
    #              self._current_card = dstCard
    #              self._pages_gen.render_card(self._current_card)
    #          else:
    #              apis.ha_api.log(f"No page with key {entity_id} found")
    #      if entity_id.startswith('navUp'):
    #          if self._previous_cards:
    #              self._current_card = self._previous_cards.pop()
    #          else:
    #              self._current_card = self._config.get_default_card()
    #          self._pages_gen.render_card(self._current_card)
    #      if entity_id.startswith('navPrev'):
    #          if self._current_card.uuid_prev:
    #              self._current_card = self._config.get_card_by_uuid(
    #                  self._current_card.uuid_prev)
    #              self._pages_gen.render_card(self._current_card)
    #      if entity_id.startswith('navNext'):
    #          if self._current_card.uuid_next:
    #              self._current_card = self._config.get_card_by_uuid(
    #                  self._current_card.uuid_next)
    #              self._pages_gen.render_card(self._current_card)
    #      elif entity_id.startswith('scene'):
    #          apis.ha_api.get_entity(entity_id).call_service("turn_on")
    #      elif entity_id.startswith('script'):
    #          apis.ha_api.get_entity(entity_id).call_service("turn_on")
    #      elif entity_id.startswith('light') or entity_id.startswith('switch') or entity_id.startswith('input_boolean') or entity_id.startswith('automation') or entity_id.startswith('fan'):
    #          apis.ha_api.get_entity(entity_id).call_service("toggle")
    #      elif entity_id.startswith('lock'):
    #          if apis.ha_api.get_entity(entity_id).state == "locked":
    #              apis.ha_api.get_entity(entity_id).call_service("unlock")
    #          else:
    #              apis.ha_api.get_entity(entity_id).call_service("lock")
    #      elif entity_id.startswith('button') or entity_id.startswith('input_button'):
    #          apis.ha_api.get_entity(entity_id).call_service("press")
    #      elif entity_id.startswith('input_select') or entity_id.startswith('select'):
    #          apis.ha_api.get_entity(entity_id).call_service("select_next")
    #      elif entity_id.startswith('vacuum'):
    #          if apis.ha_api.get_entity(entity_id).state == "docked":
    #              apis.ha_api.get_entity(entity_id).call_service("start")
    #          else:
    #              apis.ha_api.get_entity(
    #                  entity_id).call_service("return_to_base")
    #      elif entity_id.startswith('service'):
    #          apis.ha_api.call_service(entity_id.replace(
    #              'service.', '', 1).replace('.', '/', 1), **entity_config.data)
    #
    #  # for media page
    #  if button_type == "media-next":
    #      apis.ha_api.get_entity(entity_id).call_service("media_next_track")
    #  if button_type == "media-back":
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "media_previous_track")
    #  if button_type == "media-pause":
    #      apis.ha_api.get_entity(entity_id).call_service("media_play_pause")
    #  if button_type == "media-OnOff":
    #      if apis.ha_api.get_entity(entity_id).state == "off":
    #          apis.ha_api.get_entity(entity_id).call_service("turn_on")
    #      else:
    #          apis.ha_api.get_entity(entity_id).call_service("turn_off")
    #  if button_type == "media-shuffle":
    #      suffle = not apis.ha_api.get_entity(entity_id).attributes.shuffle
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "shuffle_set", shuffle=suffle)
    #  if button_type == "volumeSlider":
    #      pos = int(value)
    #      # HA wants this value between 0 and 1 as float
    #      pos = pos/100
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "volume_set", volume_level=pos)
    #  if button_type == "speaker-sel":
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "select_source", source=value)
    #
    #  # for light detail page
    #  if button_type == "brightnessSlider":
    #      # scale 0-100 to ha brightness range
    #      brightness = int(scale(int(value), (0, 100), (0,255)))
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "turn_on", brightness=brightness)
    #  if button_type == "colorTempSlider":
    #      entity = apis.ha_api.get_entity(entity_id)
    #      # scale 0-100 from slider to color range of lamp
    #      color_val = scale(int(
    #          value), (0, 100), (entity.attributes.min_mireds, entity.attributes.max_mireds))
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "turn_on", color_temp=color_val)
    #  if button_type == "colorWheel":
    #      apis.ha_api.log(value)
    #      value = value.split('|')
    #      color = pos_to_color(int(value[0]), int(value[1]), int(value[2]))
    #      apis.ha_api.log(color)
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "turn_on", rgb_color=color)
    #
    #  # for climate page
    #  if button_type == "tempUpd":
    #      temp = int(value)/10
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "set_temperature", temperature=temp)
    #  if button_type == "tempUpdHighLow":
    #      value = value.split("|")
    #      temp_high = int(value[0])/10
    #      temp_low = int(value[1])/10
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "set_temperature", target_temp_high=temp_high, target_temp_low=temp_low)
    #  if button_type == "hvac_action":
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          "set_hvac_mode", hvac_mode=value)
    #
    #  # for alarm page
    #  if button_type in ["disarm", "arm_home", "arm_away", "arm_night", "arm_vacation"]:
    #      apis.ha_api.get_entity(entity_id).call_service(
    #          f"alarm_{button_type}", code=value)
    #  if button_type == "opnSensorNotify":
    #      msg = ""
    #      entity = apis.ha_api.get_entity(entity_id)
    #      if "open_sensors" in entity.attributes and entity.attributes.open_sensors is not None:
    #          for e in entity.attributes.open_sensors:
    #              msg += f"- {apis.ha_api.get_entity(e).attributes.friendly_name}\r\n"
    #      self._pages_gen.send_message_page(
    #          "opnSensorNotifyRes", "", msg, "", "")
    #
    #  # for cardUnlock
    #  if button_type == "cardUnlock-unlock":
    #      curCard = self._config.get_card_by_uuid(
    #          entity_id.replace('navigate.', ''))
    #      if curCard is not None:
    #          if int(curCard.raw_config.get("pin")) == int(value):
    #              dstCard = self._config.search_card(
    #                  curCard.raw_config.get("destination"))
    #              if dstCard is not None:
    #                  if dstCard.hidden:
    #                      self._previous_cards.append(self._current_card)
    #                  self._current_card = dstCard
    #                  self._pages_gen.render_card(self._current_card)
    #
    #  if button_type == "mode-preset_modes":
    #      entity = apis.ha_api.get_entity(entity_id)
    #      preset_mode = entity.attributes.preset_modes[int(value)]
    #      entity.call_service("set_preset_mode", preset_mode=preset_mode)
    #
    #  if button_type == "mode-swing_modes":
    #      entity = apis.ha_api.get_entity(entity_id)
    #      swing_mode = entity.attributes.swing_modes[int(value)]
    #      entity.call_service("set_swing_mode", swing_mode=swing_mode)
    #
    #  if button_type == "mode-fan_modes":
    #      entity = apis.ha_api.get_entity(entity_id)
    #      fan_mode = entity.attributes.fan_modes[int(value)]
    #      entity.call_service("set_fan_mode", fan_mode=fan_mode)
    #
    #  if button_type in ["mode-input_select", "mode-select"]:
    #      entity = apis.ha_api.get_entity(entity_id)
    #      option = entity.attributes.options[int(value)]
    #      entity.call_service("select_option", option=option)
    #
    #  if button_type == "mode-light":
    #      if entity_id.startswith('uuid'):
    #          entity_config = self._config._config_entites_table.get(
    #              entity_id)
    #          entity_id = entity_config.entityId
    #      entity = apis.ha_api.get_entity(entity_id)
    #      options_list = entity_config.entity_input_config.get("effectList")
    #      if options_list is not None:
    #          option = options_list[int(value)]
    #      else:
    #          option = entity.attributes.effect_list[int(value)]
    #      entity.call_service("turn_on", effect=option)
    #
    #  if button_type == "mode-media_player":
    #      entity = apis.ha_api.get_entity(entity_id)
    #      option = entity.attributes.source_list[int(value)]
    #      entity.call_service("select_source", source=option)
    #
    #  # timer detail page
    #  if button_type == "timer-start":
    #      if value is not None:
    #          apis.ha_api.get_entity(entity_id).call_service(
    #              "start", duration=value)
    #      else:
    #          apis.ha_api.get_entity(entity_id).call_service("start")
    #  if button_type == "timer-cancel":
    #      apis.ha_api.get_entity(entity_id).call_service("cancel")
    #  if button_type == "timer-pause":
    #      apis.ha_api.get_entity(entity_id).call_service("pause")
    #  if button_type == "timer-finish":
    #      apis.ha_api.get_entity(entity_id).call_service("finish")
