//
// Copyright © 2024 Agora
// This file is part of TEN Framework, an open source project.
// Licensed under the Apache License, Version 2.0, with certain conditions.
// Refer to the "LICENSE" file in the root directory for more information.
//
#include "include_internal/ten_runtime/msg/loop_fields.h"

#include "include_internal/ten_runtime/msg/msg.h"
#include "include_internal/ten_runtime/msg/msg_info.h"
#include "ten_utils/macro/check.h"

void ten_msg_field_process_data_init(ten_msg_field_process_data_t *field,
                                     const char *field_name,
                                     ten_value_t *field_value,
                                     bool is_user_defined_properties) {
  TEN_ASSERT(field, "Invalid argument.");
  TEN_ASSERT(field_name, "Invalid argument.");
  TEN_ASSERT(field_value, "Invalid argument.");

  field->field_name = field_name;
  field->field_value = field_value;
  field->is_user_defined_properties = is_user_defined_properties;
  field->value_modified = false;
}

bool ten_raw_msg_loop_all_fields(ten_msg_t *self,
                                 ten_raw_msg_process_one_field_func_t cb,
                                 void *user_data, ten_error_t *err) {
  switch (ten_raw_msg_get_type(self)) {
    case TEN_MSG_TYPE_DATA: {
      ten_raw_msg_loop_all_fields_func_t loop_all_fields =
          ten_msg_info[ten_raw_msg_get_type(self)].loop_all_fields;
      if (!loop_all_fields) {
        return false;
      }
      return loop_all_fields(self, cb, user_data, err);
    }

    default:
      TEN_ASSERT(0, "Handle more cases: %d", self->type);
      return false;
  }

  return true;
}
