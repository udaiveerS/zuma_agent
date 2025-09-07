--
-- PostgreSQL database dump
--

\restrict cDOglakUbOeqsg1Js39Ynz4aCpDywVsggQSgeUST9oQrmYt2cBUXqwFWYAFK3ri

-- Dumped from database version 16.10
-- Dumped by pg_dump version 16.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: communities; Type: TABLE DATA; Schema: public; Owner: chatuser
--

INSERT INTO public.communities VALUES ('98df2cc3-896a-4b6c-9638-9f770c04d79d', 'sunset-ridge', 'Sunset Ridge Apartments', 'America/Los_Angeles');
INSERT INTO public.communities VALUES ('d9b7c8cc-3665-490b-960d-af8178efaf22', 'downtown-lofts', 'Downtown Lofts', 'America/New_York');


--
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: chatuser
--

INSERT INTO public.units VALUES ('10c4d277-9caa-41f3-838f-74197c744257', 'A101', 1, 1.0, 'available', NULL, 1200.00, '[]', '2025-09-06 00:31:32.34447+00', '2025-09-06 00:31:32.34447+00', 'sunset-ridge');
INSERT INTO public.units VALUES ('e7224b2c-6a32-44bc-80c6-48c806648c41', 'A102', 1, 1.0, 'occupied', NULL, 1200.00, '[]', '2025-09-06 00:31:32.34447+00', '2025-09-06 00:31:32.34447+00', 'sunset-ridge');
INSERT INTO public.units VALUES ('29729887-fc12-4390-ad1b-08ab4cfe12ab', 'A103', 1, 1.0, 'notice', '2025-08-01 00:00:00+00', 1250.00, '[]', '2025-09-06 00:31:32.34447+00', '2025-09-06 00:31:32.34447+00', 'sunset-ridge');
INSERT INTO public.units VALUES ('17b5973b-7588-45e4-a689-b42c08ed3002', 'B201', 2, 2.0, 'available', NULL, 1800.00, '[{"type": "move_in", "value": 1800, "description": "First month free"}]', '2025-09-06 00:31:32.34447+00', '2025-09-06 00:31:32.34447+00', 'sunset-ridge');
INSERT INTO public.units VALUES ('be6a8def-fa28-4088-9001-f52b3fd11e57', 'B202', 2, 2.0, 'notice', '2025-07-15 00:00:00+00', 1850.00, '[]', '2025-09-06 00:31:32.34447+00', '2025-09-06 00:31:32.34447+00', 'sunset-ridge');
INSERT INTO public.units VALUES ('b4c8e749-07ec-4be3-9c3d-e13c89f7c48f', 'L301', 2, 2.0, 'available', NULL, 2500.00, '[]', '2025-09-06 00:31:32.34447+00', '2025-09-06 00:31:32.34447+00', 'downtown-lofts');
INSERT INTO public.units VALUES ('91b9d9b5-ea3a-466b-81f5-7b83805f7bd6', 'L302', 2, 2.0, 'notice', '2025-09-01 00:00:00+00', 2600.00, '[{"type": "early_lease", "value": 200, "description": "Sign early and save $200/month"}]', '2025-09-06 00:31:32.34447+00', '2025-09-06 00:31:32.34447+00', 'downtown-lofts');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: chatuser
--



--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: chatuser
--



--
-- Data for Name: community_policies; Type: TABLE DATA; Schema: public; Owner: chatuser
--

INSERT INTO public.community_policies VALUES ('a81fce7c-fcb7-41b0-8482-b48050203d5f', 'pet', '{"cat": {"fee": 50, "allowed": true, "deposit": 200}, "dog": {"fee": 75, "allowed": true, "deposit": 300, "weight_limit": 50}}', '2025-09-06 00:31:32.34447+00', 'sunset-ridge');
INSERT INTO public.community_policies VALUES ('a5aacc15-d9fa-4d5a-b73a-bd27601f7483', 'smoking', '{"allowed": false, "designated_areas": []}', '2025-09-06 00:31:32.34447+00', 'sunset-ridge');
INSERT INTO public.community_policies VALUES ('10359b48-f853-4344-b96d-af46a521181f', 'pet', '{"cat": {"fee": 100, "allowed": true}, "dog": {"allowed": false}}', '2025-09-06 00:31:32.34447+00', 'downtown-lofts');


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: chatuser
--

INSERT INTO public.messages VALUES ('34f0ae4b-a98c-4148-a6c2-9710dd6a0bfd', '{"role": "assistant", "content": "Hello! I''m your AI assistant. How can I help you today?"}', 'assistant', true, NULL, NULL, '2025-09-05 23:31:32.306569+00');
INSERT INTO public.messages VALUES ('ec066f9c-ce3e-415e-9a6c-a0eae8b63157', '{"role": "user", "content": "Hi there! Can you help me understand how this chat system works?"}', 'user', true, NULL, NULL, '2025-09-05 23:32:32.306569+00');
INSERT INTO public.messages VALUES ('c13f6dd8-1d09-47f0-8d4b-4fa64e9bc930', '{"role": "assistant", "content": "Of course! This is a chat system built with FastAPI and PostgreSQL. You can ask me questions and I''ll respond with helpful information."}', 'assistant', true, NULL, NULL, '2025-09-05 23:33:32.306569+00');
INSERT INTO public.messages VALUES ('41497c43-6bb2-4b88-9be9-25d921b5faa8', '{"role": "user", "content": "Hello, how are you?"}', 'user', true, NULL, NULL, '2025-09-06 00:36:54.957188+00');
INSERT INTO public.messages VALUES ('331a01fa-3321-4e10-be7c-e024413ce15e', '{"role": "user", "content": "Hello, how are you?"}', 'user', true, NULL, NULL, '2025-09-06 00:38:08.354121+00');
INSERT INTO public.messages VALUES ('84b6b5b5-1594-441a-8459-0981a98edc07', '{"role": "assistant", "content": "Hello! I''m doing well, thank you for asking! How about you? Is there anything specific on your mind today, or are you just looking to chat?"}', 'assistant', true, NULL, '331a01fa-3321-4e10-be7c-e024413ce15e', '2025-09-06 00:38:08.360358+00');
INSERT INTO public.messages VALUES ('7ecd1f80-4630-4094-aa2b-4dce747b7c0c', '{"role": "user", "content": "Do you have any 2-bedroom apartments available?"}', 'user', true, NULL, NULL, '2025-09-06 00:38:35.818214+00');
INSERT INTO public.messages VALUES ('42c4e240-8e13-4d9b-b072-a2be0548ca36', '{"role": "user", "content": "Do you have any 2-bedroom apartments available?"}', 'user', true, NULL, NULL, '2025-09-06 00:40:23.02262+00');
INSERT INTO public.messages VALUES ('282d4e13-7fc8-4cb0-af9a-19ec68b9aa72', '{"role": "user", "content": "Do you have any 2-bedroom apartments available?"}', 'user', true, NULL, NULL, '2025-09-06 00:41:05.084795+00');
INSERT INTO public.messages VALUES ('7a69c2d6-959d-4c2d-adeb-2dc6f425cab0', '{"role": "assistant", "content": "We have two 2-bedroom apartments available at Sunset Ridge Apartments:\n\n1. **Unit Code: B201**\n   - **Bedrooms:** 2\n   - **Bathrooms:** 2.0\n   - **Rent:** $1,800\n   - **Availability Status:** Available\n   - **Special:** First month free!\n\n2. **Unit Code: B202**\n   - **Bedrooms:** 2\n   - **Bathrooms:** 2.0\n   - **Rent:** $1,850\n   - **Availability Status:** Notice (available from July 15, 2025)\n\nIf you''re interested in either of these units or have any questions, feel free to ask!"}', 'assistant', true, NULL, '282d4e13-7fc8-4cb0-af9a-19ec68b9aa72', '2025-09-06 00:41:05.089924+00');
INSERT INTO public.messages VALUES ('76b57eea-4d42-4df9-8375-0fc08c49af1f', '{"role": "user", "content": "I need a 2-bedroom apartment for July 1st move-in"}', 'user', true, NULL, NULL, '2025-09-06 00:43:13.379469+00');
INSERT INTO public.messages VALUES ('8ac25623-c7ba-4c52-919c-ad07f0ff63b4', '{"role": "assistant", "content": "Hi John! I found a 2-bedroom apartment available for your desired move-in date of July 1st, 2025, at Sunset Ridge Apartments:\n\n- **Unit Code:** B201\n- **Bedrooms:** 2\n- **Bathrooms:** 2.0\n- **Rent:** $1,800\n- **Availability Status:** Available\n- **Special:** First month free!\n\nIf you''re interested in this unit or have any questions, feel free to ask!"}', 'assistant', true, NULL, '76b57eea-4d42-4df9-8375-0fc08c49af1f', '2025-09-06 00:43:13.382405+00');
INSERT INTO public.messages VALUES ('a20e0d54-0cf4-42ab-b54d-671b5af8e128', '{"role": "user", "content": "I need a 2-bedroom apartment for August 1st move-in"}', 'user', true, NULL, NULL, '2025-09-06 00:43:33.546073+00');
INSERT INTO public.messages VALUES ('fbf720e0-1c79-411a-8c62-da5ee02efb3d', '{"role": "assistant", "content": "Hi Sarah! I found some 2-bedroom apartments available for your move-in date of August 1st, 2025, at Sunset Ridge Apartments:\n\n1. **Unit Code: B201**\n   - **Bedrooms:** 2\n   - **Bathrooms:** 2.0\n   - **Rent:** $1,800\n   - **Availability Status:** Available\n   - **Special:** First month free!\n\n2. **Unit Code: B202**\n   - **Bedrooms:** 2\n   - **Bathrooms:** 2.0\n   - **Rent:** $1,850\n   - **Availability Status:** Notice (available from July 15, 2025)\n\nIf you''re interested in either of these units or"}', 'assistant', true, NULL, 'a20e0d54-0cf4-42ab-b54d-671b5af8e128', '2025-09-06 00:43:33.550526+00');
INSERT INTO public.messages VALUES ('3528aa4a-66bf-4535-9a16-ed693db9ec2d', '{"role": "user", "content": "Actually, do you have any 1-bedroom apartments available?"}', 'user', true, NULL, NULL, '2025-09-06 00:52:54.631468+00');
INSERT INTO public.messages VALUES ('893ba153-eabf-4a67-890a-150026d0f670', '{"role": "assistant", "content": "Hi Sarah! I found some 1-bedroom apartments available at Sunset Ridge Apartments:\n\n1. **Unit Code: A101**\n   - **Bedrooms:** 1\n   - **Bathrooms:** 1.0\n   - **Rent:** $1,200\n   - **Availability Status:** Available\n\n2. **Unit Code: A103**\n   - **Bedrooms:** 1\n   - **Bathrooms:** 1.0\n   - **Rent:** $1,250\n   - **Availability Status:** Notice (available from August 1, 2025)\n\nIf you''re interested in any of these units or have any questions, feel free to ask!"}', 'assistant', true, NULL, '3528aa4a-66bf-4535-9a16-ed693db9ec2d', '2025-09-06 00:52:54.635283+00');
INSERT INTO public.messages VALUES ('e7c7fba7-8165-4b54-9d67-3ed7010bda6d', '{"role": "user", "content": "Show me 3-bedroom apartments please"}', 'user', true, NULL, NULL, '2025-09-06 00:56:17.571643+00');
INSERT INTO public.messages VALUES ('8e18a858-3ba0-42fa-8b4d-bb7fce1f8293', '{"role": "assistant", "content": "Hi Alice! Unfortunately, there are no 3-bedroom apartments available at Sunset Ridge for your preferred move-in date of August 1, 2025. \n\nHowever, I recommend checking back later or considering 2-bedroom options if that might work for you. If you have any other questions or need assistance with something else, feel free to ask!"}', 'assistant', true, NULL, 'e7c7fba7-8165-4b54-9d67-3ed7010bda6d', '2025-09-06 00:56:17.576927+00');
INSERT INTO public.messages VALUES ('89c8cfdf-b016-4739-a411-19bab157755f', '{"role": "user", "content": "Show me 1-bedroom apartments please"}', 'user', true, NULL, NULL, '2025-09-06 00:56:53.519511+00');
INSERT INTO public.messages VALUES ('187670fa-c73b-4254-acdc-605278b97d67', '{"role": "assistant", "content": "Hi Bob! I found some 1-bedroom apartments available at Sunset Ridge Apartments:\n\n1. **Unit Code: A101**\n   - **Bedrooms:** 1\n   - **Bathrooms:** 1.0\n   - **Rent:** $1,200\n   - **Availability Status:** Available\n\n2. **Unit Code: A103**\n   - **Bedrooms:** 1\n   - **Bathrooms:** 1.0\n   - **Rent:** $1,250\n   - **Availability Status:** Notice (available from August 1, 2025)\n\nIf you''re interested in any of these units or have any questions, feel free to ask!"}', 'assistant', true, NULL, '89c8cfdf-b016-4739-a411-19bab157755f', '2025-09-06 00:56:53.523355+00');
INSERT INTO public.messages VALUES ('e1cc7cfc-b6ee-4df8-bbcd-e333f4fc5656', '{"role": "user", "content": "Show me 3-bedroom apartments please"}', 'user', true, NULL, NULL, '2025-09-06 00:58:09.826517+00');
INSERT INTO public.messages VALUES ('deaacfe9-ec4c-40be-a281-e1761f40fe3d', '{"role": "assistant", "content": "Hi there! Unfortunately, there are no 3-bedroom apartments available at Sunset Ridge at this time. \n\nIf you''re open to considering 2-bedroom options or would like to check back later, please let me know! I''m here to help with any other questions you may have."}', 'assistant', true, NULL, 'e1cc7cfc-b6ee-4df8-bbcd-e333f4fc5656', '2025-09-06 00:58:09.831316+00');
INSERT INTO public.messages VALUES ('edf3c71d-cdb1-43a6-ae13-20abc1fd41d7', '{"role": "user", "content": "Do you have any 2-bedroom apartments available?"}', 'user', true, NULL, NULL, '2025-09-06 01:00:28.296604+00');
INSERT INTO public.messages VALUES ('6afebf00-4980-401e-87d9-d852cd43fc8d', '{"role": "assistant", "content": "Hi Emma! Yes, we have 2-bedroom apartments available at Sunset Ridge. Here are the details:\n\n1. **Unit Code: B201**\n   - **Bedrooms:** 2\n   - **Bathrooms:** 2.0\n   - **Rent:** $1,800\n   - **Availability Status:** Available\n   - **Special:** First month free!\n\n2. **Unit Code: B202**\n   - **Bedrooms:** 2\n   - **Bathrooms:** 2.0\n   - **Rent:** $1,850\n   - **Availability Status:** Notice (available from July 15, 2025)\n\nWould you like more information on pricing or details about any of these units?"}', 'assistant', true, NULL, 'edf3c71d-cdb1-43a6-ae13-20abc1fd41d7', '2025-09-06 01:00:28.302069+00');
INSERT INTO public.messages VALUES ('91048e0a-d26c-4522-a93a-7d9a81e6f339', '{"role": "user", "content": "Do you have any 2-bedroom apartments available?"}', 'user', true, NULL, NULL, '2025-09-06 01:01:13.101916+00');
INSERT INTO public.messages VALUES ('88408979-23a8-44a9-8e8d-4f293069938b', '{"role": "assistant", "content": "Hi Lisa! Yes, we have 2-bedroom apartments available: B201 and B202. Would you like to know about pricing, availability dates, or schedule a tour?"}', 'assistant', true, NULL, '91048e0a-d26c-4522-a93a-7d9a81e6f339', '2025-09-06 01:01:13.106932+00');
INSERT INTO public.messages VALUES ('f1f6151a-ec00-4caa-a95d-7b66e48baca6', '{"role": "user", "content": "What are the prices for those apartments?"}', 'user', true, NULL, NULL, '2025-09-06 01:01:27.370636+00');
INSERT INTO public.messages VALUES ('3a73087a-949f-4b3d-9651-752bf95025de', '{"role": "assistant", "content": "Hi Lisa! Yes, we have 2-bedroom apartments available: B201 and B202. \n\n- **B201**: Rent is $1,800 with the first month free!\n- **B202**: Rent is $1,850, available from July 15, 2025.\n\nWould you like to know more about any specific unit or schedule a tour?"}', 'assistant', true, NULL, 'f1f6151a-ec00-4caa-a95d-7b66e48baca6', '2025-09-06 01:01:27.374638+00');
INSERT INTO public.messages VALUES ('2af76d25-b32e-4917-befc-068ff3ef0978', '{"role": "user", "content": "What are the prices for 2-bedroom apartments?"}', 'user', true, NULL, NULL, '2025-09-06 01:06:27.693204+00');
INSERT INTO public.messages VALUES ('7ae1fc33-c230-47a2-9328-2e8cafd3d012', '{"role": "assistant", "content": "Hi Mike! Yes, we have 2-bedroom apartments available: B201 and B202. \n\nUnit B201: $1,800/month with first month free\n\nUnit B202: $1,850/month, available July 15th\n\nWould you like to know more about any specific unit or schedule a tour?"}', 'assistant', true, NULL, '2af76d25-b32e-4917-befc-068ff3ef0978', '2025-09-06 01:06:27.697652+00');
INSERT INTO public.messages VALUES ('ada46e6c-a585-43b1-8caf-ba5f39c686b4', '{"role": "user", "content": "Do you have any 1-bedroom apartments?"}', 'user', true, NULL, NULL, '2025-09-06 01:06:42.443055+00');
INSERT INTO public.messages VALUES ('b8bb8991-4d47-4f9f-b54e-22fd2e31275f', '{"role": "assistant", "content": "Hi Sarah! Yes, we have 1-bedroom apartments available at Sunset Ridge:\n\nUnit A101: $1,200/month, available now\n\nUnit A103: $1,250/month, available from August 1, 2025\n\nWould you like to know more about any specific unit or schedule a tour?"}', 'assistant', true, NULL, 'ada46e6c-a585-43b1-8caf-ba5f39c686b4', '2025-09-06 01:06:42.448424+00');


--
-- PostgreSQL database dump complete
--

\unrestrict cDOglakUbOeqsg1Js39Ynz4aCpDywVsggQSgeUST9oQrmYt2cBUXqwFWYAFK3ri

